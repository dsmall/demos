# This Python file uses the following encoding: utf-8
"""
    I2C LCD Library
    ~~~~~~~~~~~~~~~
    Support for JeeLabs i2c LCD Plug and HD44780 LCD
    dsmall 6 July 2012, 1 June 2013
    Has been tested with a 16 x 2 LCD but should work with up to 20 x 4 LCD
    When reading from a 40 x 2 LCD, line1 is [data0] + [data2] and line2 is [data1] + [data3]
    See http://web.alfredstate.edu/weimandn/lcd/lcd_addressing/lcd_addressing_index.html
"""

from flask import Blueprint, render_template, request
public = Blueprint('lib_i2c_lcd', __name__, template_folder='templates')

from i2c import _i2cRead, _i2cWrite

# LCD Plug chip address
LCD = 0x24
# On power on the MCP23008 IOCON reg defaults to 0x0
# We disable SEQOP (bit5 = 1) and set INT to open drain (bit2 = 1)
# Our reset function checks this value to see whether the LCD needs to be initialised
MCP_IOCON_INIT = 0x24

# MCP23008 registers
MCP_IODIR = 0x00
MCP_IOCON = 0x05
MCP_GPIO = 0x09

# MCP23008 outputs P4-P7 (P0-P3 are data)
MCP_BACKLIGHT = 0x80
MCP_ENABLE = 0x40       # Pulse high to write to HD44780
MCP_OTHER = 0x20
MCP_REGSEL = 0x10       # 1=LCD data, 0=LCD command

# HD44780 command registers
LCD_CLR = 0x01
LCD_HOME = 0x02
LCD_MODE = 0x04
LCD_DISPLAY = 0x08
LCD_SHIFT = 0x10
LCD_FUNCTION = 0x20
LCD_CGADDR = 0x40
LCD_DDADDR = 0x80


def _write4bits(rs, value):
    data = value | MCP_BACKLIGHT | rs
    _i2cWrite(LCD, MCP_GPIO, data, 'B')
    _i2cWrite(LCD, MCP_GPIO, data | MCP_ENABLE, 'B')
    _i2cWrite(LCD, MCP_GPIO, data, 'B')

def writeByte(rs, value):
    _write4bits(rs, (value >> 4) & 0x0f)
    _write4bits(rs, value & 0x0f)

def writeCmd(value):
    writeByte(0, value)
    
def writeData(value):
    writeByte(MCP_REGSEL, value)
    
# With gratitude to http://joshuagalloway.com/lcd.html
# who explains how to do this clearly and concisely
# See also Hitachi HD4487U specification, page 46
def init():
    # Set MCP IO Control register (SREAD disabled, INT to ODR)
    _i2cWrite(LCD, MCP_IOCON, MCP_IOCON_INIT, 'B')
    # Set MCP IO Direction register to output (all pins)
    # A side-effect is to enable backlight on first write to MCP_GPIO
    _i2cWrite(LCD, MCP_IODIR, 0, 'B')

    # Set to 4-bit mode (Hitachi magic)
    _write4bits(0, 0x03)
    _write4bits(0, 0x03)
    _write4bits(0, 0x03)
    _write4bits(0, 0x02)

    # 001x xx-- set interface length: 4 bits, 2 lines
    # bit 4: 8-bit(1)/4-bit(0)
    # bit 3: 1 line(0)/2 lines(1)
    # bit 2: font 5x10(1)/5x7(0)
    writeCmd(LCD_FUNCTION | 0x08)

    # 0000 1xxx enable display/cursor: display off, cursor off, blink off
    # bit 2: display on
    # bit 1: display cursor
    # bit 0: blinking cursor
    writeCmd(LCD_DISPLAY)

    # 0000 0001 clear display, home cursor
    writeCmd(LCD_CLR)

    # 0000 01xx set cursor move direction: inc cursor, do not shift data
    # bit 1: inc(1)/dec(0)
    # bit 0: shift display
    writeCmd(LCD_MODE | 0x02)
    
    # 0000 1xxx enable display/cursor: display on, cursor off, blink off
    # bit 2: display on
    # bit 1: display cursor
    # bit 0: blinking cursor
    writeCmd(LCD_DISPLAY | 0x04)

# Backlight is controlled by toggling MCP23008 P7 IO status
# Set P7 to output (0 = on) or input (1 = off)
def setBacklight(state = True):
    if state:
        _i2cWrite(LCD, MCP_IODIR, 0, 'B')
    else:
        _i2cWrite(LCD, MCP_IODIR, MCP_BACKLIGHT, 'B')

def getBacklight():
    return ((_i2cRead(LCD, MCP_IODIR, 'B') & MCP_BACKLIGHT) == 0)

# Simulate LCD for read back
_sim_mem = [' '] * 128
_sim_cur = 0

def _simSetCursor(cur):
    global _sim_cur
    _sim_cur = cur

def _simClear():
    global _sim_mem, _sim_cur
    _sim_mem = [' '] * 128
    _sim_cur = 0

def _simWrite(ch):
    global _sim_mem, _sim_cur
    if ord(ch) == 0xdf:
         ch = '°'
    _sim_mem[_sim_cur] = ch
    _sim_cur += 1
    if 0x27 < _sim_cur < 0x40:
        _sim_cur = 0x40
    elif _sim_cur > 0x67:
        _sim_cur = 0

def _simRead():
    return (''.join(_sim_mem[0x00:0x13]), ''.join(_sim_mem[0x40:0x53]),
            ''.join(_sim_mem[0x14:0x27]), ''.join(_sim_mem[0x54:0x67]))
# End of simulation

def setCursor(row, col):
    rowstart = [ 0x00, 0x40, 0x14, 0x54 ]
    writeCmd(LCD_DDADDR | (rowstart[row] + col))
    _simSetCursor(rowstart[row] + col)

def reset(clear = True):
    # Check if LCD has been initialised
    if _i2cRead(LCD, MCP_IOCON, 'B') == MCP_IOCON_INIT:
        if clear:
            writeCmd(LCD_CLR)
            _simClear()
        else:
            setCursor(0, 0)
    else:
        init()
        _simClear()

def writeString(s):
    for i in s:
        writeData(ord(i))
        _simWrite(i)


@public.route('/send-to-i2c-lcd', methods=['POST'])
def send_to_i2c_lcd():
    reset()
    writeString(request.form['line1'])
    setCursor(1, 0)
    writeString(request.form['line2'])
    if 'line3' in request.form:
        setCursor(2, 0)
        writeString(request.form['line3'])
        setCursor(3, 0)
        writeString(request.form['line4'])
    return 'OK', 200

@public.route('/clear-i2c-lcd', methods=['POST'])
def clear_i2c_lcd():
    reset()
    return 'OK', 200

# Should only need to call this if the LCD gets stuck
@public.route('/init-i2c-lcd', methods=['POST'])
def init_i2c_lcd():
    init()
    return 'OK', 200

@public.route('/backlight-i2c-lcd', methods=['POST'])
def backlight_i2c_lcd():
    import json
    if 'state' in request.form:
        setBacklight(json.loads(request.form['state']))
    return json.dumps(getBacklight())

@public.route('/read-from-i2c-lcd', methods=['POST'])
def read_from_i2c_lcd():
    import json
    try:
        return json.dumps(_simRead())
    except Exception, e:
        print '## read_from_i2c_lcd ## Unexpected error: %s' % str(e)
    return 'Bad request', 400


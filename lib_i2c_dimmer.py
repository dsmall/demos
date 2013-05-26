"""
    I2C Dimmer Library
    ~~~~~~~~~~~~~~~
    Support for JeeLabs i2c Dimmer Plug with PCA9635 LED Driver
    dsmall 13 Aug 2012, 10 May 2013

    The PCA9635 is an I2C-bus controlled 16-bit LED driver optimized for Red/Green
    /Blue/Amber (RGBA) color mixing applications. Each LED output has its own 8-bit 
    resolution (256 steps) fixed frequency individual PWM controller that operates 
    at 97 kHz with a duty cycle that is adjustable from 0 % to 99.6 % to allow the 
    LED to be set to a specific brightness value. An additional 8-bit resolution 
    (256 steps) group PWM controller has both a fixed frequency of 190 Hz and an 
    adjustable frequency between 24 Hz to once every 10.73 seconds with a duty cycle 
    that is adjustable from 0 % to 99.6 % that is used to either dim or blink all 
    LEDs with the same value.
    
    Each LED output can be off, on (no PWM control), set at its individual PWM 
    controller value or at both individual and group PWM controller values. The LED 
    output driver is programmed to be either open-drain with a 25 mA current sink 
    capability at 5 V or totem-pole with a 25 mA sink, 10 mA source capability at
    5 V. The PCA9635 operates with a supply voltage range of 2.3 V to 5.5 V and the 
    outputs are 5.5 V tolerant. LEDs can be directly connected to the LED output (up 
    to 25 mA, 5.5 V) or controlled with external drivers and a minimum amount of 
    discrete components for larger current or higher voltage LEDs. 
"""

from flask import Blueprint, render_template, request
public = Blueprint('lib_i2c_dimmer', __name__, template_folder='templates')

PCA_INC_NONE = 0
PCA_INC_ALL = 0x80      # 0x00-0x1B (28)
PCA_INC_BRI = 0xA0      # 0x02-0x11 (16)
PCA_INC_GCR = 0xC0      # 0x12-0x13 (2)
PCA_INC_BRI_GCR = 0xE0  # 0x02-0x13 (18)

@public.route('/dimmer', methods=['POST'])
def dimmer():
    import json, pytronics
    try:
        if 'command' in request.form:
            command = request.form['command']
            if command == 'read_status':
                return json.dumps(pytronics.i2cRead(0x40, PCA_INC_ALL | 0, 'I', 28))
            elif command == 'set_brightness':
                ireg = int(request.form['register'], 0)
                ival = int(request.form['value'], 0)
                pytronics.i2cWrite(0x40, ireg, ival, 'B')
                return 'OK', 200
    except Exception as e:
        print '## dimmer ##: {0}'.format(e)
    return 'Internal server error', 500

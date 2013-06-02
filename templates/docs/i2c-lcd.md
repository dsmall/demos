### I2C LCD Plug  ###

--

The I2C LCD Plug is a small board manufactured by [JeeLabs][jl] and also available from [Modern Device][md]. 
It contains an [MCP23008][mcp23008] I/O expander which connects to most common 16-pin character LCD displays
that use the [HD44780][hd44780] standard.

This application can write to the LCD display, clear it and toggle the backlight. The LCD is initialised automatically but
can be re-initialised if it gets stuck. The library maintains a virtual copy of the LCD controller memory which you
can read to see what the LCD is displaying.

A two-wire I<sup>2</sup>C bus running at 3.3V is used as interconnect, with the power and signal
lines brought out to to both sides of the board to allow daisy-chaining with other JeeLabs plugs.
The LCD Plug can be directly connected to a Rascal:

![Diagram](/static/images/docs/LCDPlug-Rascal.png)

You can run the LCD off 3V3 or 5V by setting the LOGIC and LIGHT jumpers 
on the board to +3 or HI, respectively.
To use 5V, connect pin P on the board to the 5V pin on the Rascal. 

Note that if you don't have pull-up resistors on the I<sup>2</sup>C bus
(e.g. as provided by the Sparkfun TMP-102 breakout board) you may need to add them, typically
using 1K resistors from SDA and SCL to +3V3, along with a 0.1 uF decoupling capacitor between +3V3 and GND.

#### Example Code ####

This program communicates with the LCD Plug by sending POST requests to the Rascal library `lib_i2c_lcd.py`,
for example:

    $('#send-to-lcd').click(function () {
        "use strict";
        $.post('/send-to-i2c-lcd',
            { line1: $('#line1').val(), line2: $('#line2').val() });
    });

The Rascal Python library clears the LCD, then writes the two lines of data:

    @public.route('/send-to-i2c-lcd', methods=['POST'])
    def send_to_i2c_lcd():
        reset()
        writeString(request.form['line1'])
        setCursor(1, 0)
        writeString(request.form['line2'])
        return 'OK', 200

To see how this data gets written to the LCD, please refer to the library source. The library writes
to the LCD in 4-bit mode which is explained on page 46 of the [HD44780 data sheet][hitachi].

<small>dsmall 27 May 2013</small>

[jl]: http://jeelabs.com/products/lcd-plug
[md]: http://shop.moderndevice.com/products/jeelabs-lcdplug
[mcp23008]: http://ww1.microchip.com/downloads/en/DeviceDoc/21919e.pdf
[hd44780]: http://en.wikipedia.org/wiki/Hitachi_HD44780_LCD_controller
[hitachi]: http://lcd-linux.sourceforge.net/pdfdocs/hd44780.pdf

<script type="text/javascript">
    $(document).ready(function () {
        $('#doc-content a')
            .attr('target', '_blank');
    });
</script>

### I2C LED Dimmer Plug  ###

--

The I2C LED Dimmer Plug is a small board manufactured by [JeeLabs][jl] and also available from [Modern Device][md]. 
It uses an NXP [PCA9635][pca9635] LED PWM driver optimized for color mixing. Each of the sixteen LED outputs
has its own 8-bit resolution (256 steps) PWM controller to allow its brightness to be set. In addition, a group PWM
controller can either dim or blink all LEDs. The PCA9635 operates from 3.3V, allowing direct connection
to the Rascal, but the LEDs can be run off 5V (up to 25mA).

One of the advantages of this device is that it can control the colour and brightness of up to four RGBA or
five RGB LEDs and that the settings are maintained for as long as power is applied, without further intervention
from the Rascal. This demo application automatically initialises the device if necessary, reads the present settings
and allows the colour and brightness of an RGB LED to be controlled.

A two-wire I<sup>2</sup>C bus running at 3.3V is used as interconnect, with the power and signal
lines brought out to to both sides of the board to allow daisy-chaining with other JeeLabs plugs.
The Dimmer Plug can be directly connected to a Rascal:

![Diagram](/static/images/docs/DimmerPlug-Rascal.png)

A 5V supply for the LEDs is provided by connecting pin P on the board to the 5V pin on the Rascal. 
Common Anode LEDs are required for 5V working. The demo uses a diffused 5mm Super Flux Piranha Common Anode RGB LED
from [oomlaut][ooml]. Simlar LEDs are available from [adafruit][ada] and other suppliers. For the demo,
the 5V common anode is connected to pin 1 of the output socket and the red, green and blue LEDs connected
via 270R resistors (which oomlaut includes) to pins 2, 3 and 4, respectively:

![Diagram](/static/images/docs/Dimmer-LED-Rascal.png)

Connected as above, the red, green and blue LEDs will be on channels `PWM0`, `PWM1` and `PWM2`, respectively which the
demo initialises to Pantone Process Blue `rgb(0, 51, 78)`.

Note that if you don't have pull-up resistors on the I<sup>2</sup>C bus
(e.g. as provided by the Sparkfun TMP-102 breakout board) you may need to add them, typically
using 1K resistors from SDA and SCL to +3V3, along with a 0.1 uF decoupling capacitor between +3V3 and GND.

#### Example Code ####

This program communicates with the Dimmer Plug by sending POST requests to the Rascal library `lib_i2c_dimmer.py`.
Each colour wheel writes individually to the appropriate register. For example, the red wheel writes to
register `0x02 (PWM0)` using a POST request:

    $.post('/dimmer', { command: 'set_brightness', register: reg, value: value });

The Rascal library interface is:

    @public.route('/dimmer', methods=['POST'])
    def dimmer():
        try:
            if not initialised:
                init()
            if 'command' in request.form:
                command = request.form['command']
                if command == 'read_status':
                    return json.dumps(i2cRead(0x40, PCA_INC_ALL | 0, 'I', 28))
                elif command == 'set_brightness':
                    ireg = int(request.form['register'], 0)
                    ival = int(request.form['value'], 0)
                    i2cWrite(0x40, ireg, ival, 'B')
                    return 'OK', 200
        except Exception as e:
            print '## dimmer ## Unexpected error {0}'.format(e)
        return 'Bad request', 400

When the demo starts up, it sends a `read_status` request and updates the colour wheels.

<small>dsmall 2 June 2013</small>

[jl]: http://jeelabs.com/products/dimmer-plug
[md]: http://shop.moderndevice.com/products/jeelabs-dimmer-plug
[pca9635]: http://www.nxp.com/documents/data_sheet/PCA9635.pdf
[ooml]: http://www.oomlout.co.uk/5mm-rgb-leds-super-flux-x3-p-203.html
[ada]: http://www.adafruit.com/products/314

<script type="text/javascript">
    $(document).ready(function () {
        $('#doc-content a')
            .attr('target', '_blank');
    });
</script>

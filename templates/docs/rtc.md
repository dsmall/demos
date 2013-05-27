### JeeLabs RTC Plug  ###

--

The RTC Plug is a small board containing a low power real-time clock with battery backup
manufactured by [JeeLabs][jl] and also available from [Modern Device][md]. It continues 
to track the time with second by second resolution while powered off if the optional battery is fitted.
This application can set the date and time on Rascal and RTC from an Internet [NTP][ntp] server
or, if the Rascal isn't connected to the Internet, can set Rascal date and time from the RTC.
The application can also use the RTC as a stopwatch.

The plug is based on the [DS1340][ds1340] real-time clock/calendar.
A two-wire I<sup>2</sup>C bus running at 3.3V is used as interconnect, with the power and signal
lines brought out to to both sides of the board to allow daisy-chaining with other JeeLabs plugs.
The RTC Plug can be directly connected to a Rascal:

![Diagram](/static/images/docs/RTCPlug-Rascal.png)

Note that if you don't have pull-up resistors on the I<sup>2</sup>C bus
(e.g. as provided by the Sparkfun TMP-102 breakout board) you may need to add them, typically
using 1K resistors from SDA and SCL to +3V3, along with a 0.1 uF decoupling capacitor between +3V3 and GND.

#### Example Code ####

This program communicates with the RTC Plug by sending POST requests to the Rascal library `lib_i2c_rtc.py`,
for example:

    function read_rtc() {
        "use strict";
        $.post('/rtc', function (response) {
            display_time(JSON.parse(response));
        });
    }

with the JavaScript function `display_time` is responsible for unpacking the BCD date and time from the response and displaying it.

The Rascal Python library reads the date and time from RTC Plug via the I<sup>2</sup>C bus using the Pytronics `i2cRead` function, then returns it as a JSON-encoded array, for example:

    @public.route('/rtc', methods=['POST'])
    def rtc():
        from pytronics import i2cRead, i2cWrite
        import json
        return json.dumps(i2cRead(0x68, 0, 'I', 7))

<small>dsmall 25 May 2013</small>

[jl]: http://jeelabs.com/products/rtc-plug
[md]: http://shop.moderndevice.com/products/jeelabs-rtc-plug
[ntp]: http://www.pool.ntp.org/en/
[ds1340]: http://datasheets.maximintegrated.com/en/ds/DS1340-DS1340C.pdf

<script type="text/javascript">
    $(document).ready(function () {
        $('#doc-content a')
            .attr('target', '_blank');
    });
</script>

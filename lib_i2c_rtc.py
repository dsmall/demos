"""
    I2C RTC Library
    ~~~~~~~~~~~~~~~
    Support for JeeLabs i2c RTC Plug with DS1340
    dsmall 31 July 2012, 10 May 2013
"""
from flask import Blueprint, render_template, request
public = Blueprint('lib_i2c_rtc', __name__, template_folder='templates')

def BCD(b):
    return ((b / 10) << 4) + (b % 10)

def set_rtc ():
    from pytronics import i2cWrite
    import subprocess, time
    cmd = 'ntpdate uk.pool.ntp.org'
    subp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    try:
        data = subp.communicate()[0].strip()
        t = time.gmtime()
        rtc = []
        rtc.append(BCD(t.tm_sec))
        rtc.append(BCD(t.tm_min))
        rtc.append(BCD(t.tm_hour))
        rtc.append(BCD(t.tm_wday + 1))
        rtc.append(BCD(t.tm_mday))
        rtc.append(BCD(t.tm_mon))
        rtc.append(BCD(t.tm_year - 2000))
        i2cWrite(0x68, 0, rtc, 'I')
        # Reset OSF (oscillator stopped flag)
        i2cWrite(0x68, 0x09, 0, 'B')
    except Exception, e:
        print '## set_rtc ## Unexpected error: %s' % str(e)

@public.route('/rtc', methods=['POST'])
def rtc():
    from pytronics import i2cRead, i2cWrite
    import json
    if 'command' in request.form:
        command = request.form['command']
        if command == 'set_rtc':
            set_rtc()
        elif command == 'start':
            i2cWrite(0x68, 0, i2cRead(0x68, 0) & 0x7f)
        elif command == 'stop':
            i2cWrite(0x68, 0, i2cRead(0x68, 0) | 0x80)
        elif command == 'reset':
            i2cWrite(0x68, 0, [0x80, 0, 0], 'I')
    return json.dumps(i2cRead(0x68, 0, 'I', 7))

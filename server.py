from flask import Flask, render_template, request
from uwsgidecorators import *
import time

public = Flask(__name__)

def toggle_pin(pin):
    from pytronics import read_pin, set_pin_high, set_pin_low
    if read_pin(pin) == '1':
        set_pin_low(pin)
    else:
        set_pin_high(pin)

@rbtimer(60)
def fetch_calendar(num):
    import thermostat
    thermostat.update_calendar_file()
    print('Calendar reload attempt')

@rbtimer(3)
def update_relay(num):
    import pytronics, thermostat
    actual = float(thermostat.read_sensor(0x48)) * 1.8 + 32.0
    print("Measured temperature: %f degrees" % actual)
    target = thermostat.get_target_temp('/var/www/public/static/basic.ics')
    if actual < target:
        pytronics.set_pin_high(2)
        print("Heat on")
    else:
        pytronics.set_pin_low(2)
        print("Heat off")

@public.route('/<template_name>.html')
def template(template_name):
    return render_template(template_name + '.html', magic="Hey presto!")

@public.route('/')
@public.route('/relay.html')
def index():
    import pytronics
    pin = pytronics.read_pin(2)
    (chan0, chan1, chan2, chan3) = pytronics.summarize_analog_data()
    return render_template('/relay.html', chan0=chan0, chan1=chan1, chan2=chan2, chan3=chan3, pin=pin)

@public.route('/toggle', methods=['POST'])
def toggle():
    import pytronics
    if(request.form['target_state'] == '1'):
        pytronics.set_pin_high(2)
        result = 'Pins set high'
    elif(request.form['target_state'] == '0'):
        pytronics.set_pin_low(2)
        result = 'Pins set low'
    else:
        result = 'Target_state is screwed up'
    return result

@public.route('/temperature', methods=['POST'])
def temperature():
    import json, thermostat
    data = {
        "time" : float(time.time()),
        "actual" : float(thermostat.read_sensor(0x48)),
        "target" : thermostat.get_target_temp('/var/www/public/static/basic.ics')
    }
    return json.dumps(data)

@public.route('/analog', methods=['POST'])
def analog():
    from pytronics import read_analog
    import json, time
    try:
        ad_ref = float(request.form['adref'])
    except KeyError:
        ad_ref = 3.3
    data = {
        "time" : float(time.time()),
        "A0" : float(read_analog('A0')) * ad_ref / 1024.0
    }
    return json.dumps(data)

@public.route('/send-to-lcd', methods=['POST'])
def send_to_lcd():
    import pytronics
    pytronics.send_serial(request.form['serial_text'], 9600)
    return render_template('/lcd.html')

@public.route('/clear-lcd', methods=['POST'])
def clear_lcd():
    import pytronics
    pytronics.send_serial(chr(0xFE) + chr(0x01), 9600)
    return render_template('/lcd.html')

@public.route('/set-color', methods=['POST'])
def set_color():
    import subprocess
    color = request.form['color']
    cmd = 'blinkm set-rgb -d 9 -r ' + str(int(color[0:2], 16)) + ' -g ' + str(int(color[2:4], 16)) + ' -b ' + str(int(color[4:6], 16))
    subprocess.Popen([cmd], shell=True)
    return ('color sent to Blinkm')

@public.route('/sms', methods=['POST'])
def parse_sms():
    import subprocess
    message = request.form['Body']
    print "Received text message: " + str(message)
    f = open('/var/www/public/thermostat-target.txt', 'w')
    f.write(str(message))
    f.close()
    return ('Message processed')

@public.route('/sprinkler', methods=['POST'])
def sprinkler():
    import pytronics
    message = request.form['Body']
    print message
    #command = request.form['command']
    #if(command == "ON"):
    #    pytronics.set_pin_high(2)
    #else:
    #    pytronics.set_pin_low(2)
    return ('Sprinkler toggled')

if __name__ == "__main__":
    public.run(host='127.0.0.1:5000', debug=True)

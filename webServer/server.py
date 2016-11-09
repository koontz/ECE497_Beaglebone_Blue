#!/usr/bin/env python

import socketio
import eventlet
import eventlet.wsgi
from flask import Flask, render_template
from ctypes import cdll, c_float
import Adafruit_BBIO.GPIO as GPIO

Left_line = "P9_23"
#Right_line = "P9_10"

GPIO.setup(Left_line, GPIO.IN)
#GPIO.setup(Right_line, GPIO.IN)

#the path to the robot cape library file
robo = cdll.LoadLibrary('/root/Robotics_Cape_Installer-master/libraries/libroboticscape.so')

GREEN =0
RED = 1

sio = socketio.Server()
app = Flask(__name__)
green = 0
red =0

#the webpage handling
@app.route('/')
def index():
    return render_template('base.html')


#socket.io message handling
@sio.on('connect',namespace='/')
def connect(sid, environ):
    pass
    #print("Connected",environ)

@sio.on('matrix')
def matrix(sid,message):
    sio.emit('matrix',[0])

@sio.on('brightness')
def brightness(sid,message):
    pass

@sio.on('servo')
def servo(sid,message):
    angle = (message['position'])
    robo.send_servo_pulse_normalized(message['index'],c_float(angle))

@sio.on('red',namespace='/')
def toggleRed(sid, message):
    global red
    red = red ^ 1
    robo.set_led(RED,red)
    sio.emit('red',red)

@sio.on('green',namespace='/')
def toggleRed(sid, message):
    global green
    green = green ^ 1
    robo.set_led(GREEN,green)
    sio.emit('green',red)

@sio.on('read',namespace='/')
def read(sid,message):
    result = '_'
    sensor = message['sensor']
    side = message['side']
    print(side)
    if(sensor == 'En'):
        result = 'Encoders do not work for this demo'
    elif(sensor == 'Bump'):
        if(side == 'left'):
            print(GPIO.input(Left_line))
            result = str(GPIO.input(Left_line))
        else:
            result = str(GPIO.input(Left_line))
    elif(sensor == 'Sonic'):
        if(side == 'left'):
            result = str(robo.get_adc_raw(3))
        else:
            result = str(robo.get_adc_raw(2))
    elif(sensor == 'Line'):
        if(side == 'left'):
            result = str(robo.get_adc_raw(0))
        else:
            result = str(robo.get_adc_raw(1))
    sio.emit('read',{'side': message['side'],
                     'sensor': sensor,
                     'value': result})
@sio.on('move',namespace='/')
def move(sid,message):
    throttle = 1.0
    if(message=='up'):
        robo.send_servo_pulse_normalized(4,c_float(throttle))
        robo.send_servo_pulse_normalized(3,c_float(-throttle))
    elif(message=='down'):
        robo.send_servo_pulse_normalized(4,c_float(-throttle))
        robo.send_servo_pulse_normalized(3,c_float(throttle))
    elif(message=='left'):
        robo.send_servo_pulse_normalized(4,c_float(-throttle))
        robo.send_servo_pulse_normalized(3,c_float(-throttle))
    elif(message=='right'):
        robo.send_servo_pulse_normalized(4,c_float(throttle))
        robo.send_servo_pulse_normalized(3,c_float(throttle))

if(__name__ == "__main__"):
    #starts the server
    robo.initialize_cape()
    robo.enable_servo_power_rail()
    app = socketio.Middleware(sio,app) #wraps app in socket io handling
    eventlet.wsgi.server(eventlet.listen(('',8090)),app) #starts the server
    robo.disable_servo_power_rail()
    robo.cleanup_cape()

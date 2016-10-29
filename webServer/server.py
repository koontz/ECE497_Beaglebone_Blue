#!/usr/bin/env python
import socketio
import eventlet
import eventlet.wsgi
from flask import Flask, render_template
from ctypes import cdll, c_float

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
def brightness(sid,message):
    print message
    angle = (message['position']-7)/8.0
    print angle
    print c_float(angle)
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

if(__name__ == "__main__"):
    #starts the server
    robo.initialize_cape()
    robo.enable_servo_power_rail()
    app = socketio.Middleware(sio,app) #wraps app in socket io handling
    eventlet.wsgi.server(eventlet.listen(('',8090)),app) #starts the server
    robo.disable_servo_power_rail()
    robo.cleanup_cape()

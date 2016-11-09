#!/usr/bin/env python

import socketio
import eventlet
import eventlet.wsgi
import sys
import signal
import json
import thread
import threading

from pixy import *
from ctypes import *
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

PIXY_MIN_X             =    0
PIXY_MAX_X             =  319
PIXY_MIN_Y             =    0
PIXY_MAX_Y             =  199

PIXY_X_CENTER          =  ((PIXY_MAX_X-PIXY_MIN_X) / 2)
PIXY_Y_CENTER          =  ((PIXY_MAX_Y-PIXY_MIN_Y) / 2)
PIXY_RCS_MIN_POS       =    0
PIXY_RCS_MAX_POS       = 1000
PIXY_RCS_CENTER_POS    =  ((PIXY_RCS_MAX_POS-PIXY_RCS_MIN_POS) / 2)

PIXY_RCS_PAN_CHANNEL   =    0
PIXY_RCS_TILT_CHANNEL  =    1

PAN_PROPORTIONAL_GAIN  =  400
PAN_DERIVATIVE_GAIN    =  300
TILT_PROPORTIONAL_GAIN =  500
TILT_DERIVATIVE_GAIN   =  400

BLOCK_BUFFER_SIZE      =    1

sio = socketio.Server()
app = Flask(__name__)
green = 0
red =0
global run_flag
run_flag=True
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
    print message
@sio.on('followBall',namespace='/')
def followBall(sid,message):
    global run_flag
    run_flag = 1
    thread = threading.Thread(target = lambda:trackBall())
    thread.start()

@sio.on('stopBall',namespace='/')
def stopBall(sid,message):
    global run_flag
    run_flag = 0   


def setrun_flag(value):
  global run_flag
  run_flag = value

def trackBall():
    block       = Block()
    global run_flag
    run_flag = True
    frame_index = 0
    
    while run_flag:

        # Do nothing until a new block is available #
        while not pixy_blocks_are_new() and run_flag:
            pass

        # Grab a block #
        count = pixy_get_blocks(BLOCK_BUFFER_SIZE, block)

        # Was there an error? #
        pan_error=1/100
        if count < 0:
            print 'Error: pixy_get_blocks() [%d] ' % count
            pixy_error(count)
            sys.exit(1)
            pan_error=1/100
        if count > 0:
            # We found a block #

            # Calculate the difference between Pixy's center of focus #
            # and the target.                                         #
            pan_error  = PIXY_X_CENTER - block.x
            tilt_error = block.y - PIXY_Y_CENTER

            # Apply corrections to the pan/tilt gimbals with the goal #
            # of putting the target in the center of Pixy's focus.    #
        error_scale=(pan_error*0.5*PIXY_X_CENTER)/12000
        right_angle=0.15+0.3*error_scale
        left_angle=0.15-0.3*error_scale
        
        print(c_float(left_angle))
        robo.send_servo_pulse_normalized(3,c_float(left_angle))
        robo.send_servo_pulse_normalized(4,c_float(right_angle))
        oldright=right_angle
        oldleft=left_angle
        if (frame_index % 50) == 0:
            # If available, display block data once a second #
            print 'frame %d:' % frame_index

            if count == 1:
                print '  sig:%2d x:%4d y:%4d width:%4d height:%4d' % (block.signature, block.x, block.y, block.width, block.height)
                data = {'x': block.x, 'y': block.y,'width': block.width,'height': block.height}
                with open('data.json', 'w') as outfile:
                    json.dump(data, outfile, indent=4, sort_keys=True, separators=(',', ':'))
        frame_index = frame_index + 1
def initPixy():
    pixy_init_status = pixy_init()

    if pixy_init_status != 0:
        print 'Error: pixy_init() [%d] ' % pixy_init_status
        pixy_error(pixy_init_status)
        return

if(__name__ == "__main__"):
    #starts the server
    robo.initialize_cape()
    robo.enable_servo_power_rail()
    initPixy()
    
    
    app = socketio.Middleware(sio,app) #wraps app in socket io handling
    eventlet.wsgi.server(eventlet.listen(('',8090)),app) #starts the server
    robo.disable_servo_power_rail()
    robo.cleanup_cape()

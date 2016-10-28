#!/usr/bin.env python

from ctypes import cdll
robo = cdll.LoadLibrary('/root/Robotics_Cape_Installer-master/libraries/libroboticscape.so')

if(__name__=="__main__"):
    print("testing")
    robo.set_led(0,0)
    robo.set_led(1,0)

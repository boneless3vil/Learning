#!/usr/bin/env python3
########################################################################
# Filename    : Blink.py
# Description : Basic usage of GPIO. Let led blink.
# Author      : www.freenove.com
# modification: 2019/12/28
########################################################################
import RPi.GPIO as GPIO
import time

LEDred = 11    # define ledPin
LEDblue = 22
LEDgreen = 24
LEDyellow = 26
def setup():
    GPIO.setmode(GPIO.BOARD)       # use PHYSICAL GPIO Numbering
    # set the ledPin to OUTPUT mode
    GPIO.setup(LEDred, GPIO.OUT)
    GPIO.setup(LEDblue, GPIO.OUT)
    GPIO.setup(LEDgreen, GPIO.OUT)
    GPIO.setup(LEDyellow, GPIO.OUT)
    # make ledPin output LOW level
    GPIO.output(LEDred, GPIO.LOW)
    GPIO.output(LEDblue, GPIO.LOW)
    GPIO.output(LEDgreen, GPIO.LOW)
    GPIO.output(LEDyellow, GPIO.LOW)
    print('using pin%d' % LEDred)

def loop():
    while True:
        GPIO.output(LEDred, GPIO.HIGH)  # make ledPin output HIGH level to turn on led
        print ('LEDred turned on >>>')     # print information on terminal
        time.sleep(1)                   # Wait for 1 second
        GPIO.output(LEDred, GPIO.LOW)   # make ledPin output LOW level to turn off led
        print ('LEDred turned off <<<')
        time.sleep(1)                   # Wait for 1 second

        GPIO.output(LEDblue, GPIO.HIGH)
        print ('LEDblue turned on >>>')
        time.sleep(1)
        GPIO.output(LEDblue, GPIO.LOW)
        print ('LEDblue turned off <<<')
        time.sleep(1)

        GPIO.output(LEDgreen, GPIO.HIGH)
        print ('LEDgreen turned on >>>')
        time.sleep(1)
        GPIO.output(LEDgreen, GPIO.LOW)
        print ('LEDgreen turned off <<<')
        time.sleep(1)

        GPIO.output(LEDyellow, GPIO.HIGH)
        print ('LEDyellow turned on >>>')
        time.sleep(1)
        GPIO.output(LEDyellow, GPIO.LOW)
        print ('LEDyellow turned off <<<')
        time.sleep(1)

def destroy():
    GPIO.cleanup()                      # Release all GPIO

if __name__ == '__main__':    # Program entrance
    print('Program is starting ... \n')
    setup()
    try:
        loop()
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        destroy()


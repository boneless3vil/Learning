#!/usr/bin/env python3
########################################################################
# Filename    : Blink.py
# Description : Basic usage of GPIO. Let led blink.
# Author      : www.freenove.com
# modification: 2019/12/28
########################################################################
import RPi.GPIO as GPIO
import time

# define ledPin
LEDs = {
    'LEDred': 11,
    'LEDblue': 22,
    'LEDgreen': 13,
    'LEDyellow': 26
    }

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
        for k, v in LEDs.items():
            """ LEDs turned on/off"""
            GPIO.output(v, GPIO.HIGH)
            print (f'{k} turned on >>>')     # print LED color to terminal
            time.sleep(1)                   # Wait for 1 second
            GPIO.output(v, GPIO.LOW)
            print (f'{k} turned off <<<')
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


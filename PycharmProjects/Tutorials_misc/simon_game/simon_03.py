# beginner's guide to raspberry pipe bread boarding with Simon
# https://www.makeuseof.com/beginners-guide-to-raspberry-pi-breadboarding-with-simon/

import random
import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(True) # set to False in tutorial

# color assignments to pins
red = 18
yellow = 22
green = 24
blue = 26

# not sure about this group, but perhaps assigning the word color to  output
GPIO.setup(red, GPIO.OUT)
GPIO.setup(yellow, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_UP)

game = True

while game:
    redButtonState = GPIO.input(32)
    if redButtonState == 0:
        GPIO.output(red, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(red, GPIO.LOW)

    yellowButtonState = GPIO.input(36)
    if yellowButtonState == 0:
        GPIO.output(red, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(yellow, GPIO.LOW)

    greenButtonState = GPIO.input(38)
    if greenButtonState == 0:
        GPIO.output(green, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(green, GPIO.LOW)

    blueButtonState = GPIO.input(40)
    if blueButtonState  == 0:
        GPIO.output(blue, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(blue, GPIO.LOW)




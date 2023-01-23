# beginner's guide to raspberry pipe bread boarding with Simon
# https://www.makeuseof.com/beginners-guide-to-raspberry-pi-breadboarding-with-simon/

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(True) # set to False in tutorial

red = 18
yellow = 22
green = 24
blue = 26

GPIO.setup(red, GPIO.OUT)
GPIO.setup(yellow, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

GPIO.output(red, GPIO.HIGH)
GPIO.output(yellow, GPIO.HIGH)
GPIO.output(green, GPIO.HIGH)
GPIO.output(blue, GPIO.HIGH)



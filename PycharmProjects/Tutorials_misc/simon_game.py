# Simon the 80s light game tutorial
# https://www.makeuseof.com/beginners-guide-to-raspberry-pi-breadboarding-with-simon/

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

red = 18
GPIO.setup(red, GPIO.OUT)
GPIO.output(red, GPIO.LOW)



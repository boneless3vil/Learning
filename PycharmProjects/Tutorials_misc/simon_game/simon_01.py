# beginner's guide to raspberry pipe bread boarding with Simon
# https://www.makeuseof.com/beginners-guide-to-raspberry-pi-breadboarding-with-simon/

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)    # use PHYSICAL GPIO Numbering
GPIO.setwarnings(True)  # tutorial sets this False

# attached to pin 18, so you can just call "red" instead of its pin number
red = 18
GPIO.setup(red, GPIO.OUT)   # set the ledPin (18) to OUTPUT mode

GPIO.output(red, GPIO.LOW)  # make ledPin (18) output LOW level
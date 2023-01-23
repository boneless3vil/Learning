# beginner's guide to raspberry pipe bread boarding with Simon
# https://www.makeuseof.com/beginners-guide-to-raspberry-pi-breadboarding-with-simon/

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD) # not necessary, but easier
GPIO.setwarnings(True)  # tutorial sets this False

# attached to pin 18, so you can just call "red" instead of its pin number
red = 18
GPIO.setup(red, GPIO.OUT)

# turns light off. if set to HIGH, code will turn light on.
GPIO.output(red, GPIO.LOW)
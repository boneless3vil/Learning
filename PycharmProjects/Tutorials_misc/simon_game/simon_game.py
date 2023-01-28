# Simon the 80s light game tutorial
# https://www.makeuseof.com/beginners-guide-to-raspberry-pi-breadboarding-with-simon/

import random
import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)    # use PHYSICAL GPIO Numbering
GPIO.setwarnings(False)

# COLOR assigned to physical PIN
red = 18
yellow = 22
green = 24
blue = 25

# set pins to output
GPIO.setup(red, GPIO.OUT)   # here, pin 18 set to output
GPIO.setup(yellow, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

# set button Pins to PULL UP INPUT mode
GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # this button on pin 32
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_UP)

game = True

pattern = []
lights = [red, yellow, green, blue]

while game:
    pattern.append(random.randint(0, 3))

    for x in pattern:
        GPIO.output(lights[x], GPIO.HIGH)
        time.sleep(1)
        GPIO.output(lights[x], GPIO.LOW)
        time.sleep(0.5)

    for x in pattern:
        waitingForInput = True

        while waitingForInput:
            redButtonState = GPIO.input(32)
            yellowButtonState = GPIO.input(36)
            greenButtonState = GPIO.input(38)
            blueButtonState = GPIO.input(40)

            if redButtonState == 0:
                GPIO.output(red, GPIO.HIGH)
                waitingForInput = False
                # check for player input
                if x != 0:
                    game = False
                time.sleep(1)
                GPIO.output(red, GPIO.LOW)

            if yellowButtonState == 0:
                GPIO.output(yellow, GPIO.HIGH)
                waitingForInput = False
                # check for player input
                if x != 0:
                    game = False
                time.sleep(1)
                GPIO.output(yellow, GPIO.LOW)

            if greenButtonState == 0:
                GPIO.output(green, GPIO.HIGH)
                waitingForInput = False
                # check for player input
                if x != 0:
                    game = False
                time.sleep(1)
                GPIO.output(green, GPIO.LOW)

            if blueButtonState == 0:
                GPIO.output(blue, GPIO.HIGH)
                waitingForInput = False
                # check for player input
                if x != 0:
                    game = False
                time.sleep(1)
                GPIO.output(blue, GPIO.LOW)

    time.sleep(1)






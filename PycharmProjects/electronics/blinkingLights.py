# PycharmProjects/electronics/blinkingLights.py python3
########################################################################
# Filename    : blinkingLights.py
# Description : Basic usage of GPIO. Let 4 colored leds blink.
# Author      : www.freenove.com, modified by Jonathan Baldwin
# modification: 2019/12/28, 1/28/2023
########################################################################
import RPi.GPIO as GPIO
import time

ledRED = 11     # define LED pin
ledBLUE = 22
ledGREEN = 24
ledYELLOW = 26


def setup():
    GPIO.setmode(GPIO.BOARD)

    #set the LED pin to OUTPUT mode
    GPIO.setup(ledRED, GPIO.OUT)
    GPIO.setup(ledBLUE, GPIO.OUT)
    GPIO.setup(ledGREEN, GPIO.OUT)
    GPIO.setup(ledYELLOW, GPIO.OUT)

    # Set the LED pin to LOW mode
    GPIO.output(ledRED, GPIO.LOW)
    print('using pin%d' % ledRED)
    GPIO.output(ledBLUE, GPIO.LOW)
    print('using pin%d' % ledBLUE)
    GPIO.output(ledGREEN, GPIO.LOW)
    print('using pin%d' % ledGREEN)
    GPIO.output(ledYELLOW, GPIO.LOW)
    print('using pin%d' % ledYELLOW)


def loop():
    while True:
        # Red light
        GPIO.output(ledRED, GPIO.HIGH)
        print('Red Light ON >>>>')
        time.sleep(0.100)
        GPIO.output(ledRED, GPIO.LOW)
        print('Red Light OFF <<<<')
        time.sleep(0.100)

        # Blue light
        GPIO.output(ledBLUE, GPIO.HIGH)
        print('Blue Light ON >>>>')
        time.sleep(0.100)
        GPIO.output(ledBLUE, GPIO.LOW)
        print('Blue Light OFF <<<<')
        time.sleep(0.100)

        # Green light
        GPIO.output(ledGREEN, GPIO.HIGH)
        print('Green Light ON >>>>')
        time.sleep(0.100)
        GPIO.output(ledGREEN, GPIO.LOW)
        print('Green Light OFF <<<<')
        time.sleep(0.100)

        # Yellow light
        GPIO.output(ledYELLOW, GPIO.HIGH)
        print('Yellow Light ON >>>>')
        time.sleep(0.100)
        GPIO.output(ledYELLOW, GPIO.LOW)
        time.sleep(0.100)


def destroy():  # Release all GPIO
    GPIO.cleanup()


if __name__ == '__main__':      # Program start
    print('Program is starting... \n')
    setup()
    try:
        loop()
    except KeyboardInterrupt:   # Press CTRL+C to end the program.
        destroy()


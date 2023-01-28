# blinking lights raspberry pipe project with GPIO

import RPi.GPIO as GPIO
import time

LEDred = 18     # define LEDPin
LEDblue = 22
LEDgreen = 24
LEDyellow = 26


def setup():
    GPIO.setmode(GPIO.BOARD)    # use PHYSICAL GPIO Numbering
    # set up LED pins to OUTPUT mode
    GPIO.setup(LEDred, GPIO.OUT)
    GPIO.setup(LEDblue, GPIO.OUT)
    GPIO.setup(LEDgreen, GPIO.OUT)
    GPIO.setup(LEDyellow, GPIO.OUT)
    # make LEDPin output LOW level
    GPIO.output(LEDred, GPIO.LOW)
    GPIO.output(LEDblue, GPIO.LOW)
    GPIO.output(LEDgreen, GPIO.LOW)
    GPIO.output(LEDyellow, GPIO.LOW)
    print('using pin%d'%LEDred)


def loop():
    while True:
        GPIO.output(LEDred, GPIO.HIGH)  # make LEDPin output HI level to turn on LED
        print('LED turned on >>>>')     # print information to terminal
        time.sleep(0.1)   # wait one 2nd
        GPIO.output(LEDred, GPIO.LOW)
        print('LED turned off <<<<')
        time.sleep(0.1)

        GPIO.output(LEDblue, GPIO.HIGH)  # make LEDPin output HI level to turn on LED
        print('LED turned on >>>>')     # print information to terminal
        time.sleep(0.1)   # wait one 2nd
        GPIO.output(LEDblue, GPIO.LOW)
        print('LED turned off <<<<')
        time.sleep(0.1)

        GPIO.output(LEDgreen, GPIO.HIGH)  # make LEDPin output HI level to turn on LED
        print('LED turned on >>>>')     # print information to terminal
        time.sleep(0.1)   # wait one 2nd
        GPIO.output(LEDgreen, GPIO.LOW)
        print('LED turned off <<<<')
        time.sleep(0.1)

        GPIO.output(LEDyellow, GPIO.HIGH)  # make LEDPin output HI level to turn on LED
        print('LED turned on >>>>')     # print information to terminal
        time.sleep(0.1)   # wait one 2nd
        GPIO.output(LEDyellow, GPIO.LOW)
        print('LED turned off <<<<')
        time.sleep(0.1)


def destroy():
    GPIO.cleanup()  # Release all GPIO


if __name__ == '__main __':
    print('Program is starting... \n')
    setup()
    try:
        loop()
    except KeyboardInterrupt:   # Press CTRL-C in the program.
        destroy()

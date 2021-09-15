import RPi.GPIO as GPIO
import time

BTN1 = 5
BTN2 = 6

GPIO.setup(BTN1, GPIO.IN)
GPIO.setup(BTN2, GPIO.IN)

while True:
    if GPIO.input(BTN1) == 1:
        print('1 1')
    else:
        print('1 0')

    if GPIO.input(BTN2) == 1:
        print('2 1')
    else:
        print('2 0')

    time.sleep(0.1)

import RPi.GPIO as GPIO


class Gpio:
    IN = GPIO.IN
    OUT = GPIO.OUT
    HIGH = GPIO.HIGH
    LOW = GPIO.LOW

    def __init__(self) -> None:
        super().__init__()

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

    def setup(self, pin, mode) -> None:
        GPIO.setup(pin, mode)

    def output(self, pin, state) -> None:
        GPIO.output(pin, state)

    def input(self, pin):
        return GPIO.input(pin)

from settings import settings
from lib.gpio import Gpio


class Buttons:
    BUTTON_RED = settings['btn_red']['pin']
    BUTTON_BLACK = settings['btn_black']['pin']

    def __init__(self, gpio: Gpio):
        self.GPIO = gpio
        self.GPIO.setup(self.BUTTON_RED, self.GPIO.IN)
        self.GPIO.setup(self.BUTTON_BLACK, self.GPIO.IN)

    def read(self, pin) -> bool:
        return self.GPIO.input(pin) == Gpio.HIGH

    def read_black(self) -> bool:
        return self.read(self.BUTTON_RED)

    def read_red(self) -> bool:
        return self.read(self.BUTTON_BLACK)
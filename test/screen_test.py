from lib.gpio import Gpio

gpio = Gpio()

gpio.setup(13, GPIO.OUT)
gpio.output(pin, 1)

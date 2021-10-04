from lib.gpio import Gpio
from lib.screen import Screen
from lib.buttons import Buttons
from lib.player import Player
from service.buttonController import ButtonController
from settings import settings
import time

import threading

gpio = Gpio()
screen = Screen(gpio)
event = threading.Event()

screen.screen_off()


def start_handler():
    screen.screen_on()


def stop_handler():
    screen.screen_off()


player = Player(start_handler=start_handler, stop_handler=stop_handler, event=event)


def button_handler(red_reading, black_reading):
    settings['debug'] and print('btn press detected')
    if player.is_running():
        player.stop_now()

    while player.is_running():
        time.sleep(0.2)

    if red_reading:
        settings['debug'] and print('1btn read')
        player.start(settings['videos'][0], settings['video_timeout'])

    if black_reading:
        settings['debug'] and print('2btn read')
        player.start(settings['videos'][1], settings['video_timeout'])


button_controller = ButtonController(Buttons(gpio), event)
button_controller.set_handler(button_handler)

if __name__ == '__main__':
    button_controller.start()


from . import baseService
import lib.buttons as libbuttons
import threading
import time


class ButtonController(baseService.BaseService):
    LOCK_TIME = 5

    def __init__(
            self,
            buttons: libbuttons.Buttons,
            event: threading.Event
    ):
        super().__init__()

        self.t = None
        self.stop = False
        self.handler = None
        self.buttons = buttons
        self.event = event
        self.lastLockTime = time.time()

    def set_handler(self, handler):
        self.handler = handler

    def start(self):
        self.stop = False
        self.t = threading.Thread(
            target=self.worker,
            daemon=True,
            args=(
                self.handler,
                self.stop,
            )
        )
        self.t.start()

    def stop(self):
        self.stop = True

    def worker(self, handler, stop):
        print('starting')
        print('asd')
        print('stop: ')
        while True and not self.stop:
            print('running')
            now = time.time()
            if now - self.lastLockTime < self.LOCK_TIME:
                print('skipping')
                continue

            red_reading = self.buttons.read_red()
            black_reading = self.buttons.read_black()

            if red_reading or black_reading:
                print('handling')
                self.lastLockTime = now
                handler(red_reading, black_reading)
            self.event.wait(0.1)

        print('stopping')

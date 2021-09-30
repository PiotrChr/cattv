import pyglet
from settings import settings
import numpy.core.multiarray
import cv2
import numpy as np
import time
import random
import subprocess
import json


window = pyglet.window.Window()


class Player:
    def __init__(self, start_handler=None, stop_handler=None):
        self.resolution = settings['resolution']
        self.window_name = "cattv_player"
        self.start_handler = start_handler
        self.stop_handler = stop_handler
        self.capture = None
        self.start_time = None
        self.stop = False
        self.duration = 0
        self.fps = 1

        # self.init()

    def is_running(self):
        return self.capture.isOpened()

    def load(self, media):
        self.capture = cv2.VideoCapture('../' + media)

        if not self.capture.isOpened():
            print("Error opening video  file")

        (duration, fps) = self.get_media_info(media)

        self.duration = duration
        self.fps = fps

    def init(self):
        cv2.namedWindow(self.window_name, cv2.WINDOW_FREERATIO)
        # cv2.namedWindow(self.window_name, cv2.WND_PROP_FULLSCREEN)
        # cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def set_frame(self, frame):
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, frame)

    def get_media_info(self, media):
        result = subprocess.check_output(
            f'ffprobe -v quiet -show_streams -select_streams v:0 -of json "{media}"',
            shell=True).decode()
        fields = json.loads(result)['streams'][0]

        duration = float(fields['tags']['DURATION'])
        fps = float(eval(fields['r_frame_rate']))

        return duration, fps

    def get_random_frame(self):
        return random.randint(0, int(self.duration * self.fps))

    def get_frame(self, start_time, fps):
        return start_time * fps

    def stop(self):
        self.stop = True

    def should_stop(self, timeout):
        return self.start_time + timeout > time.time() or self.stop

    def play_random(self, media, timeout):
        self.start_handler()

        self.load(media)
        self.start_time = time.time()

        self.set_frame(self.get_random_frame())

        while self.capture.isOpened():
            # Capture frame-by-frame
            ret, frame = self.capture.read()
            if ret:
                new_frame = cv2.resize(frame, self.resolution, interpolation=cv2.INTER_AREA)
                # Display the resulting frame
                cv2.imshow(self.window_name, new_frame)

                # Press Q on keyboard to  exit
                if (cv2.waitKey(25) & 0xFF == ord('q')) or self.should_stop(timeout):
                    break

            # Break the loop
            else:
                break

        self.stop = False
        self.capture.release()

        # Closes all the frames
        cv2.destroyAllWindows()
        self.stop_handler()

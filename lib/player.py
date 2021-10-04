from settings import settings
import numpy.core.multiarray
import cv2
import time
import random
import subprocess
import json
from settings import settings
import threading


class Player:
    def __init__(self, start_handler=None, stop_handler=None, event=None):
        self.resolution = settings['resolution']
        self.window_name = "cattv_player"
        self.start_handler = start_handler
        self.stop_handler = stop_handler
        self.capture = None
        self.start_time = None
        self.duration = 0
        self.fps = 1
        self.t = None
        self.event = event

    def is_running(self):
        return self.capture and self.capture.isOpened()

    def start(self, media, timeout):
        settings['debug'] and print('starting player thread')
        self.stop = False
        self.t = threading.Thread(
            target=self.play_random,
            daemon=True,
            args=(
                media,
                timeout
            )
        )
        self.t.start()

    def load(self, media):
        if settings['debug']:
            print('loading media: ')
            print(media)

        self.init()
        self.capture = cv2.VideoCapture(media)

        if not self.capture.isOpened():
            print("Error opening video file")

        (duration, fps) = self.get_media_info(media)

        self.duration = duration
        self.fps = fps

    def init(self):
        cv2.namedWindow(self.window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def set_frame(self, frame):
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, frame)

    def get_media_info(self, media):
        result = subprocess.check_output(
            f'ffprobe -v quiet -show_streams -select_streams v:0 -of json "{media}"',
            shell=True).decode()
        fields = json.loads(result)['streams'][0]

        duration = float(fields['duration'])
        fps = float(eval(fields['r_frame_rate']))

        return duration, fps

    def get_random_frame(self):
        random_frame = random.randint(0, int(self.duration * self.fps))
        if settings['debug']:
            print('fps', self.fps)
            print('duration: ', self.duration)
            print('duration frames: ', self.duration * self.fps)
            print('random_frame: ', random_frame)
        return random_frame

    def get_frame(self, start_time, fps):
        return start_time * fps

    def stop_now(self):
        settings['debug'] and print('received external stop signal')
        self.t.do_stop = True

    def should_stop(self, timeout):
        return self.start_time + timeout < time.time() or getattr(self.t, 'do_stop', False)

    def play_random(self, media, timeout):

        settings['debug'] and print('start handler')
        self.start_handler()

        self.load(media)
        self.start_time = time.time()

        settings['debug'] and print('setting frame')
        self.set_frame(self.get_random_frame())
        settings['debug'] and print('playing random')
        while self.capture.isOpened():
            # Capture frame-by-frame
            ret, frame = self.capture.read()
            if ret:
                new_frame = cv2.resize(frame, self.resolution, interpolation=cv2.INTER_AREA)
                # Display the resulting frame
                cv2.imshow(self.window_name, new_frame)

                # Press Q on keyboard to  exit
                if (cv2.waitKey(25) & 0xFF == ord('q')) or self.should_stop(timeout):
                    settings['debug'] and print('received quit signal')
                    self.t.do_stop = False
                    break

            # Break the loop
            else:
                settings['debug'] and print('no return frame')
                break

        self.t.do_stop = False
        self.capture.release()

        settings['debug'] and print('closing all')
        # Closes all the frames
        cv2.destroyAllWindows()
        self.stop_handler()

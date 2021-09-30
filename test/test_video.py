# importing libraries
import cv2
import subprocess
import json
import random
import time


VID = '../resources/1.mp4'
# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture(VID)


def get_media_info(media):
    result = subprocess.check_output(
        f'ffprobe -v quiet -show_streams -select_streams v:0 -of json "{media}"',
        shell=True).decode()
    fields = json.loads(result)['streams'][0]

    duration = float(fields['duration'])
    fps = float(eval(fields['r_frame_rate']))

    return duration, fps


(duration, fps) = get_media_info(VID)
random_frame = random.randint(0, int(duration * fps))

window_name = "window"

W = 656
H = 512

# Check if camera opened successully
if (cap.isOpened()== False):
    print("Error opening video  file")

cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
print(random_frame, duration, fps)
cap.set(cv2.CAP_PROP_POS_FRAMES, random_frame)
# Read until video is completed

start_time = time.time()
duration = 15

def should_stop():
    return start_time + duration < time.time()

while cap.isOpened():
    print('starting')
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:

        new_frame = cv2.resize(frame, (W, H), interpolation=cv2.INTER_AREA)
        # Display the resulting frame
        cv2.imshow(window_name, new_frame)

        # Press Q on keyboard to  exit
        if (cv2.waitKey(25) & 0xFF == ord('q')) or should_stop():
            print('closing')
            break

    # Break the loop
    else:
        print(ret)
        print('not ok')
        break

# When everything done, release
# the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
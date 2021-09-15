# importing libraries
import cv2
import numpy as np

# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture('../resources/1.mp4')

window_name = "window"

W = 2880
H = 1800

# Check if camera opened successully
if (cap.isOpened()== False):
    print("Error opening video  file")

cv2.namedWindow(window_name, cv2.WINDOW_FREERATIO)
# cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Read until video is completed
while(cap.isOpened()):

    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:

        new_frame = cv2.resize(frame, (W, H), interpolation=cv2.INTER_AREA)
        # Display the resulting frame
        cv2.imshow(window_name, new_frame)

        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break

# When everything done, release
# the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
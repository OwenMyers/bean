import os
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import sys
import RPi.GPIO as gpio
from time import sleep

led_pin = 21

gpio.setmode(gpio.BCM)
gpio.setup(led_pin, gpio.OUT)
gpio.output(led_pin, 1)

#IM_WIDTH = 1280
#IM_HEIGHT = 720
IM_WIDTH = 640
IM_HEIGHT = 480


camera_type = 'picamera'
parser = argparse.ArgumentParser()
parser.add_argument('--usbcam', help='Use a USB webcam instead of picamera',
                    action='store_true')
args = parser.parse_args()
if args.usbcam:
    camera_type = 'usb'


# sys.path.append('..')


from utils import visualization_utils as vis_util

CWD_PATH = os.getcwd()

frame_rate_calc = 1
freq = cv2.getTickFrequency()
font = cv2.FONT_HERSHEY_SIMPLEX

if camera_type == 'picamera':
    # Initialize Picamera and grab reference to the raw capture
    camera = PiCamera()
    camera.resolution = (IM_WIDTH, IM_HEIGHT)
    camera.framerate = 10
    rawCapture = PiRGBArray(camera, size=(IM_WIDTH, IM_HEIGHT))
    rawCapture.truncate(0)

    for frame1 in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        t1 = cv2.getTickCount()

        frame = np.copy(frame1.array)
        original = np.copy(frame1.array)
        frame.setflags(write=1)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_expanded = np.expand_dims(frame_gray, axis=0)
        
        gaussian_blur = cv2.GaussianBlur(frame_gray, (5, 5), 0)
        (min_val, max_val, min_loc, max_loc) = cv2.minMaxLoc(frame_gray)

        cv2.circle(original, max_loc, 10, (255, 0, 0), 2)

        #vis_util.visualize_boxes_and_labels_on_image_array(
        #    frame,
        #    np.squeeze(boxes),
        #    np.squeeze(classes).astype(np.int32),
        #    np.squeeze(scores),
        #    category_index,
        #    use_normalized_coordinates=True,
        #    line_thickness=8,
        #    min_score_thresh=0.40)

        cv2.putText(frame, "FPS: {0:.2f}".format(frame_rate_calc), (30, 50), font, 1, (255, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('Object detector', original)

        t2 = cv2.getTickCount()
        time1 = (t2 - t1) / freq
        frame_rate_calc = 1 / time1

        if cv2.waitKey(1) == ord('q'):
            break

        rawCapture.truncate(0)

    camera.close()

    camera.release()

cv2.destroyAllWindows()

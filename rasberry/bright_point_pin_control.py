import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as gpio
from time import sleep

#IM_WIDTH = 1280
#IM_HEIGHT = 720
IM_WIDTH = 640
IM_HEIGHT = 480

NO_MOVEMENT_BUFF_PERCENT_HEIGHT = 50
NO_MOVEMENT_BUFF_PERCENT_WIDTH = 50


def main():
    gpio.setmode(gpio.BCM)
    gpio.setup(output_pin_x1, gpio.OUT)
    gpio.setup(output_pin_x2, gpio.OUT)
    gpio.setup(output_pin_y1, gpio.OUT)
    gpio.setup(output_pin_y2, gpio.OUT)
    gpio.output(output_pin_x1, 0)
    gpio.output(output_pin_x2, 0)
    gpio.output(output_pin_y1, 0)
    gpio.output(output_pin_y2, 0)

    frame_rate_calc = 1
    freq = cv2.getTickFrequency()
    font = cv2.FONT_HERSHEY_SIMPLEX

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
        # frame looks like [HEIGHT, WIDTH, ___]
        # max_loc looks like [horizontal, vertical] (i.e. width, height)
        # if outside in positive x direction trigger positive x pin
        if max_loc[0] > x_positive_buff:
            gpio.output(output_pin_x2, 0)
            gpio.output(output_pin_x1, 1)
        # otherwise set the pin to off
        else:
            gpio.output(output_pin_x1, 0)

        # if outside in negative x direction trigger negative x pin
        if max_loc[0] < x_negative_buff:
            gpio.output(output_pin_x1, 0)
            gpio.output(output_pin_x2, 1)
        # otherwise set the pin to off
        else:
            gpio.output(output_pin_x2, 0)

        # if outside in positive y direction trigger positive y pin
        if max_loc[1] > y_positive_buff:
            gpio.output(output_pin_y2, 0)
            gpio.output(output_pin_y1, 1)
        # otherwise set the pin to off
        else:
            gpio.output(output_pin_y1, 0)

        # if outside in netative y direction trigger negative y pin
        if max_loc[1] < y_negative_buff:
            gpio.output(output_pin_y1, 0)
            gpio.output(output_pin_y2, 1)
        # otherwise set the pin to off
        else:
            gpio.output(output_pin_y2, 0)

        cv2.putText(
            frame,
            "FPS: {0:.2f}".format(frame_rate_calc),
            (30, 50),
            font,
            1,
            (255, 255, 0),
            2,
            cv2.LINE_AA
        )
        cv2.imshow('Object detector', original)

        t2 = cv2.getTickCount()
        time1 = (t2 - t1) / freq
        frame_rate_calc = 1 / time1

        if cv2.waitKey(1) == ord('q'):
            break

        rawCapture.truncate(0)

        if cv2.waitKey(1) == ord('q'):
            break

    camera.close()
    camera.release()
    gpio.cleanup()

    cv2.destroyAllWindows()

if __name__ == '__main__':
    # positive x movement
    output_pin_x1 = 21
    # negative x movement
    output_pin_x2 = 20
    # positive y movement
    output_pin_y1 = 24
    # negative y movement
    output_pin_y2 = 23


    center_x = IM_WIDTH/2
    center_y = IM_HEIGHT/2

    x_positive_buff = center_x + center_x * float(NO_MOVEMENT_BUFF_PERCENT_WIDTH) / 100.0
    x_negative_buff = center_x - center_x * float(NO_MOVEMENT_BUFF_PERCENT_WIDTH) / 100.0
    x_positive_buff = round(x_positive_buff)
    x_negative_buff = round(x_negative_buff)

    y_positive_buff = center_y + center_y * float(NO_MOVEMENT_BUFF_PERCENT_HEIGHT) / 100.0
    y_negative_buff = center_y - center_y * float(NO_MOVEMENT_BUFF_PERCENT_HEIGHT) / 100.0
    y_positive_buff = round(y_positive_buff)
    y_negative_buff = round(y_negative_buff)

    main()

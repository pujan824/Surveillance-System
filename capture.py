import numpy 
import cv2
import cv2.cv as cv
import sys
import time 
import os

def main (argv):
    '''
    need to change feed location to actual cameras
    '''
    feed = null
    feed = str(sys.argv[1])

    os.system(feed)

    print("OpenCV applied")
    print("url:" + feed)

    capture = cv2.VideoCapture(feed)
    capture.set(cv.CV_CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 480)

    if not capture.isOpened():
        try:
            capture.open()
        except ValueError:
            print("Can not open video. Check url and connection")
            exit()
    print("Video is streaming")
from imutils.video import VideoStream # used to capture the video
from imutils.video import FPS # stream the video output, keep track of number of frames
import argparse               # processed per second
import imutils
import time
import cv2
from datetime import datetime, time
import numpy as np
import time as time2

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="webcam filter.mp4") # location of the video to analyse
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
ap.add_argument("-t", "--tracker", type=str, default="csrt", help="OpenCV object tracker type")
args = vars(ap.parse_args())
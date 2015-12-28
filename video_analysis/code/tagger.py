## from http://docs.opencv.org/master/d7/d8b/tutorial_py_lucas_kanade.html#gsc.tab=0
import numpy as np
import pandas as pd
import cv2
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import math


#cap = cv2.VideoCapture('slow.flv')
#cap = cv2.VideoCapture('media/GOPR0081.MP4')
cap = cv2.VideoCapture('../media/CKeLfaOl0Qk.mp4')
# Create some random colors
color = np.random.randint(0,255,(100,3))
pylab.ion()
num_frames = 5
i_frame = 0
while(i_frame < num_frames):

    for j in range(3):
        for i in range(10):
            ret,frame = cap.read()


        img = frame
        #cv2.imshow("image", img)
        plt.figure(figsize=(4,3))
        plt.imshow(img)
        plt.show()

    i_frame += 1
    key = cv2.waitKey(0) & 0xFF

    if key == ord('x'):
        print "Yay!"
    elif key == ord('q'):
        print "quit!"
        break

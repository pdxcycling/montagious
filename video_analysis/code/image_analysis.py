import cv2
import io
import base64
from IPython.display import HTML



## class ImageDetection
## Blur detection
def variance_of_laplacian(image):
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
    return cv2.Laplacian(image, cv2.CV_64F).var()


video = io.open('media/GP030969.MP4', 'r+b').read()
encoded = base64.b64encode(video)
HTML(data='''<video alt="test" controls>
                <source src="data:video/mp4;base64,{0}" type="video/mp4" />
             </video>'''.format(encoded.decode('ascii')))


## from http://docs.opencv.org/master/d7/d8b/tutorial_py_lucas_kanade.html#gsc.tab=0
import numpy as np
import cv2
import matplotlib.pyplot as plt

cap = cv2.VideoCapture('media/GOPR0084.MP4')

# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 25,
                        qualityLevel = 0.5,
                        minDistance = 10,
                        blockSize = 7 )

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 5,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Create some random colors
color = np.random.randint(0,255,(100,3))

# Take first frame and find corners in it
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)

num_frames = 1000
i_frame = 0
while(i_frame < num_frames):
    ret,frame = cap.read()
    #frame = cv2.GaussianBlur(frame,(99,99),0)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    print "Frame Number: ", 1



    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    # Select good points
    good_new = p1[st==1]
    good_old = p0[st==1]

    print(type(mask))
    print(type(good_new))
    print(type(good_old))

    # draw the tracks
    for i,(new,old) in enumerate(zip(good_new,good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
        print("Mask before: " + str(type(mask)))
        #NOTE: I don't think drawing functions return anything - they're edit-in-place, methinks
        # http://docs.opencv.org/2.4/modules/core/doc/drawing_functions.html
        #mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
        cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
        #print("Mask after : " + str(type(mask)))
        #frame = cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
        cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
        img = cv2.add(frame,mask)

    print type(frame)

    #plt.imshow(img)
    #plt.imshow(frame_gray)
    plt.figure(figsize=(20,12))
    plt.imshow(img)
    plt.show()
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

    # Now update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1,1,2)

    i_frame += 1

cv2.destroyAllWindows()
cap.release()

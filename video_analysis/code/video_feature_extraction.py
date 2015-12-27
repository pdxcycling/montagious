import numpy as np
import pandas as pd
from scene_analysis import SceneAnalysis
from video_utilities import VideoUtilities
import cv2

class VideoFeatureExtraction(object):
    '''
    '''

    def __init__(self):
        '''
        Default constructor
        '''
        pass

    @staticmethod
    def run(video_id, video):
        '''
        INPUT:
        path to video file (mp4 format)
        OUTPUT:
        dataframe with frame-by-frame analysis
        '''

        ## Go through every frame in the video and extract features
        cap = cv2.VideoCapture(video)
        frame = None

        ## Output dataframe
        video_df = pd.DataFrame()

        num_frames = cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
        i_frame = 0
        while i_frame < num_frames:
            ## Progress logging
            #if i_frame % 100 == 0:
            #print i_frame

            if frame is not None:
                prev_frame = frame.copy()
            else:
                prev_frame = None

            ret,frame = cap.read()
            ## If there are no more frames, break out of loop
            if ret == False:
                break

            frame_series = pd.Series()
            frame_series['video_id'] = video_id
            frame_series['frame_number'] = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES-1) ## -1 because this is index of *next* frame
            frame_series['time'] = cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC) / 1000.

            ## Blur
            blur_df = SceneAnalysis.get_blur(frame)

            ## Color Spectrum
            color_df = SceneAnalysis.get_hsv_hists(frame)

            ## Optical Flow
            if prev_frame is not None:
                flow_df = VideoUtilities.optical_flow_on_frame(frame, prev_frame)
            else:
                flow_df = None

            ## Merge results into single dataframe
            #video_df = video_df.append(pd.concat([frame_series, blur_df, color_df, flow_df], axis=1, ignore_index=True))
            #video_df = video_df.append(frame_series)
            #cat['video_id'] = video_id
            cat = pd.concat([blur_df, color_df, flow_df], axis=1)
            cat['video_id'] = video_id
            cat['frame_number'] = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES-1)
            cat['time'] = cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC) / 1000.
            #cat = pd.concat([frame_series, cat], axis=1)
            video_df = video_df.append(cat, ignore_index=True)

            i_frame += 1

        ## Pickle model and save it to S3 or local directory
        return video_df

if __name__ == "__main__":
    ## Testing for a simple example
    video_df = VideoFeatureExtraction.run('id 1', '../media/GOPR0081.MP4')
    print video_df

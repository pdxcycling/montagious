import pandas as pd
from video_utilities import VideoUtilities
from preprocess import Preprocess

class Video(object):
    def __init__(self, video_id, video_file):
        '''
        Default constructor
        '''
        self.video_id = video_id
        self.video_file = video_file
        self.audio_file = Preprocess.separate_audio(video_id, video_file)
        self.optical_flow = VideoUtilities.optical_flow(video_file)

    def read(self):
        '''
        Read video file
        '''
        pass

    def preprocess(self, video):
        '''
        while video has another image
            call _img_preprocess
            store result in frames DF
        '''
        pass

    def _img_preprocess(self, image):
        '''
        Pipeline for cleaning of raw images
        '''
        processed = image.copy()
        # Convert to grayscale to eliminate auto-adjustment artifacts
        processed = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
        # Blur to reduce spurious (minor) image artifacts
        processed = cv2.GaussianBlur(old_gray,(15,15),0)
        return processed

if __name__ == "__main__":
    v = Video('Test', '~/data_science_class/project_exploration/playground/snowboarding.mp4')

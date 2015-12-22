import cv2
import io
import base64
from IPython.display import HTML
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests

class VideoAnalysis(object):
    '''
    TODO:
    - Define common interfaces on similar functions
    - Define what format video will come in as
    - Probably want a preprocessed dataframe with image, time, (and maybe features)
    '''

    def __init__(self):
        '''
        '''
        self.features = pd.DataFrame()

    @staticmethod
    def detect_cut(video):
        '''
        Cut detection
        NOTE: This is a tough problem in and of itself.
              This will require a machine learning algorithm all to itself.
              Egads.
        TODO: Using simple thresholding, flag everything that could potentially be a Cut
              Perhaps by optical flow mean distance
              Then cut these scenes out (some frames before, some frames after) automatically and then hand-review them
              This creates our training set
              Then we train a model on this
        '''
        pass

    @staticmethod
    def detect_shake(video):
        '''
        Shake detection
        '''
        pass

    @staticmethod
    def detect_blur(video):
        '''
        Detect blur
        '''
        pass

    @staticmethod
    def optical_flow(video):
        '''
        Optical flow - useful for preprocessing
        Should this go here? Or should this be in preprocessing???
        '''
        pass

    @staticmethod
    def synchrony(video):
        '''
        Audio/Visual Synchrony
        '''
        pass

    @staticmethod
    def find_faces(video):
        '''
        Find faces in the images
        '''
        pass


    ## Top Level: pipeline
    ## TODO: should this go in a separate file?

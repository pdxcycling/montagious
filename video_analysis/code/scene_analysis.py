import pandas as pd
import numpy as np
import cv2

class SceneAnalysis(object):
    '''
    This encapsulate all methods to process a single image in a video

    TODO:
    -
    '''

    ## Blur Detection
    ## From: http://
    @staticmethod
    def get_blur(image):
        # compute the Laplacian of the image and then return the focus
        # measure, which is simply the variance of the Laplacian
        ## TODO: Machine learning to determine the proper threshold
        ##       of Blur vs. non-Blur
        out = pd.DataFrame([cv2.Laplacian(image, cv2.CV_64F).var()], columns=['blur'])
        return out

    @staticmethod
    def get_hsv_hists(image):
        '''
        Hue, Saturation, Value
        INPUT
            image - RGB image
        OUTPUT

        '''
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        hue_df = SceneAnalysis._get_hist(hsv[:,:,0].ravel(), num_bins=72, max_val=180, prefix="hue_bin_")
        sat_df = SceneAnalysis._get_hist(hsv[:,:,1].ravel(), num_bins=25, max_val=255, prefix="sat_bin_")
        val_df = SceneAnalysis._get_hist(hsv[:,:,2].ravel(), num_bins=25, max_val=255, prefix="val_bin_")
        out = pd.concat([hue_df, sat_df, val_df], axis=1)
        return out

    @staticmethod
    def _get_hist(hsv_image, num_bins, max_val, prefix):
        '''
        '''
        ##max_val= hsv_image.max()
        hist, bins = np.histogram(hsv_image.ravel(), num_bins, [0,max_val])
        out = pd.DataFrame(index=[0])
        out = pd.DataFrame(np.array([hist.ravel()]))#.apply(lambda x: float(x)).T
        out.columns = [prefix + str(v) for v in bins[:-1]]
        return out

    ## Face Detection
    ## return locations of possible faces...?
    ##   with potential certainty?
    ## return whether scene contains a face...?
    @staticmethod
    def find_faces(images):
        pass

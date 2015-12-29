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


    # @staticmethod
    # def get_hsv_hists(image, bw_mask=True):
    #     '''
    #     Hue, Saturation, Value
    #     INPUT
    #         image - RGB image
    #     OUTPUT
    #     '''
    #     hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    #     hue_df = SceneAnalysis._get_hist(hsv[:,:,0].ravel(), num_bins=72, max_val=180, prefix="hue_bin_")
    #     sat_df = SceneAnalysis._get_hist(hsv[:,:,1].ravel(), num_bins=25, max_val=255, prefix="sat_bin_")
    #     val_df = SceneAnalysis._get_hist(hsv[:,:,2].ravel(), num_bins=25, max_val=255, prefix="val_bin_")
    #     out = pd.concat([hue_df, sat_df, val_df], axis=1)
    #     return out


    @staticmethod
    def get_hsv_hists(image, bw_mask=True):
        '''
        Hue, Saturation, Value, White Pixels, Black Pixels
        INPUT
            image - RGB image
        OUTPUT

        '''
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        mask, bw_count_df = SceneAnalysis._get_filter_bw(hsv)

        ## Mask off black and white values
        ## Black/white values may affect color hist
        ## NOTE: saturation and value do not need to be masked
        hue_df = hsv[:,:,0] * mask

        ## Create binned value counts per HSV channel
        hue_hist_df = SceneAnalysis._get_hist(hue_df.ravel(), num_bins=72, max_val=180, prefix="hue_bin_")
        sat_hist_df = SceneAnalysis._get_hist(hsv[:,:,1].ravel(), num_bins=25, max_val=255, prefix="sat_bin_")
        val_hist_df = SceneAnalysis._get_hist(hsv[:,:,2].ravel(), num_bins=25, max_val=255, prefix="val_bin_")
        out = pd.concat([hue_hist_df, sat_hist_df, val_hist_df, bw_count_df], axis=1)
        return out

    @staticmethod
    def _get_filter_bw(hsv_image):
        '''
        Black/White filter
        INPUT:
        OUTPUT:
        '''
        ## Create dataframe for black and white pixels
        bw_df = pd.DataFrame(index=[0])
        ## Pixels with 'value' component less than 10 (out of 255) are marked as black
        v_mask = (hsv_image[:,:,2] > 10)
        bw_df['num_black_pixels'] = np.sum(v_mask == 0)
        ## Pixels with 'saturation' component less than 10 (out of 255) are marked as white
        s_mask = (hsv_image[:,:,1] > 10)
        bw_df['num_white_pixels'] = np.sum(s_mask + (v_mask == 0) == 0)         ## remove black pixels from calculations

        ## Create a mask of 1's (non-black/white pixel) and 0's (black/white pixel)
        mask = s_mask * v_mask
        vec_function = np.vectorize(lambda x: 1 if x > 0 else -1)
        mask = vec_function(mask)
        return mask, bw_df

    @staticmethod
    def _get_hist(hsv_image, num_bins, max_val, prefix):
        '''
        INPUT:
        OUTPUT:
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

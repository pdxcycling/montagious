import pandas as pd

class SceneAnalysis(object):
    '''
    This encapsulate all methods to process a single image in a video

    TODO:
    -
    '''

    ## Blur Detection
    ## From: http://
    def get_blur(image):
        # compute the Laplacian of the image and then return the focus
        # measure, which is simply the variance of the Laplacian
        ## TODO: Machine learning to determine the proper threshold
        ##       of Blur vs. non-Blur
        return cv2.Laplacian(image, cv2.CV_64F).var()

    ## Color spectrum detection
    def get_color_spectrum(image):
        '''
        What does this really mean?
          - Mean color?
          - Color distribution
        '''
        pass

    ## Brightness
    def get_brightness(image):
        '''
        Average brightness of image
        '''

    ## Frequencies present

    ## Face Detection
    ## return locations of possible faces...?
    ##   with potential certainty?
    ## return whether scene contains a face...?
    def find_faces(images):
        pass

import cv2 as cv

def get_optimal_font_scale(text, width):    #using this function to get the optimal fontScale so that it can fit images with different resolutions
    for scale in reversed(range(59,10,-1)):
        textSize = cv.getTextSize(text, fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=scale/10, thickness=2)
        new_width = textSize[0][0]
        if (new_width <= width):
            return scale/10
        return 0.90
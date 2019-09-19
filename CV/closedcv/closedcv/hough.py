import cv2
import numpy as np
import copy
import math

def find_lines(img: np.ndarray, rho: int, theta: int, thresh: int, if_canny: bool=True)->np.ndarray:
    """ Find lines in input image 
    
    Arguments:
        img {np.ndarray} -- input image, for better results must be in grayscale
        rho {int} --  Distance resolution of the accumulator in pixels.
        theta {int} -- Angle resolution of the accumulator in radians
        thresh {int} -- Accumulator threshold parameter. Only those lines are returned that get enough votes ( >\texttt{threshold} ).
        if_canny {bool} -- If canny operator should be applied to image 
    Returns:
        np.ndarray -- Image with lines on it
    """
    new_img = copy.deepcopy(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if if_canny:
        edges = cv2.Canny(gray,50,250,apertureSize = 3)
    else:
        edges = gray
    lines = cv2.HoughLinesP(edges,rho,theta,thresh)
    max_line = None
    min_line = None
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(new_img,(x1,y1),(x2,y2),(255,0,0),2)
        
        cv2.circle(new_img, (x1, y1), 3, (0,255,0), -1)
        cv2.circle(new_img, (x2, y2), 3, (0,255,0), -1)
        dist = math.hypot(x2-x1, y2-y1)
        if not max_line or dist>max_line:
            max_line = dist
        if not min_line or dist<min_line:
            min_line = dist
    stats = {'max': max_line, 'min': min_line, 'count': len(lines)}
    return new_img, stats
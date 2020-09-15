import cv2
from closedcv.hough import *

if __name__=="__main__":
    img = cv2.imread('./input/sud.jpeg')
    dir_ = './res/'
    
    lines, stats = find_lines(img, 0.5, np.pi/180, 10)
    cv2.imwrite(dir_ + 'lines_1.jpg', lines) 
    print(stats)
        
    img = cv2.imread('./input/index.png')
    
    lines, stats = find_lines(img, 0.5, np.pi/180, 10)
    cv2.imwrite(dir_ + 'lines_2.jpg', lines)
    print(stats)
    
    img = cv2.imread('./input/sud.jpeg')

    lines, stats = find_lines(img, 10, np.pi/180, 500, False)
    cv2.imwrite(dir_ + 'lines_1_no_canny.jpg', lines) 
    print(stats)
    
    img = cv2.imread('./input/index.png')
    print(stats)
    
    lines, stats = find_lines(img, 20, np.pi/180, 500, False)
    cv2.imwrite(dir_ + 'lines_2_no_canny.jpg', lines)

    img = cv2.imread('./input/circles.png')

    circ = find_circle(img, 100, 30, 30, 15, False)
    cv2.imwrite(dir_ + 'circles_1.jpg', circ)    
    
    img = cv2.imread('./input/aero.jpeg')

    circ = find_circle(img, 100, 30, 30, 15, False)
    cv2.imwrite(dir_ + 'aero_1.jpeg', circ)
    
    img = cv2.imread('./input/nardi.jpg') 
    
    circ = find_circle(img, 100, 30, 30, 15, False)
    cv2.imwrite(dir_ + 'nardi_1.jpeg', circ)   

    img = cv2.imread('./input/circles.png')

    circ = find_circle(img, 100, 30, 30, 15)
    cv2.imwrite(dir_ + 'circles_1_canny.jpg', circ)    
    
    img = cv2.imread('./input/aero.jpeg')

    circ = find_circle(img, 100, 30, 30, 15)
    cv2.imwrite(dir_ + 'aero_1_canny.jpeg', circ)
    
    img = cv2.imread('./input/nardi.jpg') 
    
    circ = find_circle(img, 100, 30, 30, 15)
    cv2.imwrite(dir_ + 'nardi_1_canny.jpeg', circ) 
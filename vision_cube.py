"""

# -*- coding: utf-8 -*-
"""
@author: hugop
"""



import cv2
import numpy as np
from math import atan2, cos, sin, sqrt, pi
 



def cube_rouge_detection(hsv, result1, result2):
    # create a binary thresholded image on hue between red and yellow
    lower = (0,150,150)
    upper = (15,255,255)
    thresh = cv2.inRange(hsv, lower, upper)

    # apply morphology
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,9))
    clean = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15,15))
    clean = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # get external contours
    contours = cv2.findContours(clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]


    for c in contours:
        cv2.drawContours(result1,[c],0,(0,0,0),5)
        # get rotated rectangle from contour
        rot_rect = cv2.minAreaRect(c)
        if c.shape[0] > 50 :   #on veut des caré de au mooins 50 pixel de contour
            print("c.shape",c.shape[0])
        
            box = cv2.boxPoints(rot_rect)
            (x,y),(MA,ma),angle = cv2.fitEllipse(c)
            #print("rouge_angle",angle)
            box = np.int0(box)
            # draw rotated rectangle on copy of img
            
            cv2.drawContours(result2,[box],0,(2,2,220),4)
            #getOrientation(c, result2)
            
            M = cv2.moments(box)
            if M['m00'] != 0.0:
                x = int(M['m10']/M['m00'])
                y = int(M['m01']/M['m00'])
                #print("jaune",x,y)
                result2[y,x,0] = 255
                result2[y,x,1] = 255
                result2[y,x,2] = 255
    return result2,result1

     
    return result2,result1
    
def cube_jaune_detection(hsv, result1, result2):
    # create a binary thresholded image on hue between red and yellow
    lower = (25,100,100)
    upper = (45,255,255)
    thresh = cv2.inRange(hsv, lower, upper)
    cv2.imshow("jaune- thresh",  thresh)
    # apply morphology
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,9))
    clean = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15,15))
    clean = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # get external contours
    contours = cv2.findContours(clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]


    for c in contours:
        
        if c.shape[0] > 50 :   #on veut des caré de au mooins 50 pixel de contour
            cv2.drawContours(result1,[c],0,(0,0,0),2)
            # get rotated rectangle from contour
            rot_rect = cv2.minAreaRect(c)
            #print("jaune_c",c)
            print("c.shape",c.shape[0])
        
            box = cv2.boxPoints(rot_rect)
            (x,y),(MA,ma),angle = cv2.fitEllipse(c)
            print("jaune_angle",angle)
            box = np.int0(box)
            # draw rotated rectangle on copy of img
            cv2.drawContours(result2,[box],0,(15,255,220),2)
            M = cv2.moments(box)
            if M['m00'] != 0.0:
                x = int(M['m10']/M['m00'])
                y = int(M['m01']/M['m00'])
                #print("jaune",x,y)
                result2[y,x,0] = 255
                result2[y,x,1] = 255
                result2[y,x,2] = 255
    return result2,result1
        
     
    # save result



#main 

image = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('inditification_cube3.avi', fourcc,20.0, (640,  480))


while True:
  ret, img = image.read()
  
  if ret == True:


    result_jaune = img.copy()
    result_rouge = img.copy()
    result2 = img.copy()
# convert to HSV, since red and yellow are the lowest hue colors and come before green
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    result2,contour_rouge = cube_rouge_detection(hsv, result_rouge, result2)
    result2,contour_jaune = cube_jaune_detection(hsv, result_jaune, result2)


    # display result
    
    cv2.imshow("result2", result2)
    cv2.imshow("rouge", contour_rouge)
    cv2.imshow("jaune", contour_jaune)
    
    
    # write the flipped frame
    out.write(result2)
    

  if cv2.waitKey(20) == ord('q'):
    break

out = cv2.VideoWriter(result2, cv2.VideoWriter_fourcc(*'MP4V'),20.0, (640,480))
result2.release()
contour_rouge.release()
contour_jaune.release()
out.release()

cv2.destroyAllWindows()

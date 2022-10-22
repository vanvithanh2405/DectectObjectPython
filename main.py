import cv2 
from tracker import *
import numpy as np

#Create tracker object
tracker = EuclideanDistTracker()

cap = cv2.VideoCapture('nap-chai.mp4')

# Object dectection from stable camera 
while True:
    ret, frame = cap.read()
    #Extract Region of interest
    roi = frame[180:440,130:300]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _,threshold = cv2.threshold(gray_roi,150,255,cv2.THRESH_BINARY)
    detections = []
    #Object Detection
    contours,_ = cv2.findContours(threshold,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        #Calculate area and remove small element
        area = cv2.contourArea(cnt)
        if area > 850:
            # cv2.drawContours(roi, [cnt],-1,(0,255,0),2)
            x, y, w, h = cv2.boundingRect(cnt)

            detections.append([x, y, w, h])

    # 2. Object Tracking
    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv2.putText(roi, str(id), (x, y), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)
    
    cv2.imshow("gray_roi",gray_roi)
    cv2.imshow("Frame", frame)
    cv2.imshow("Threshold", threshold)
 
    key = cv2.waitKey(30)
    if key == 27:
        break
    
cap.realease()
cv2.destroyAllWindows()
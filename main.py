import cv2
from tracker import *
import numpy as np

# Create tracker object
tracker = EuclideanDistTracker()

cap = cv2.VideoCapture('nap-chai-3.mp4')


# Object dectection from stable camera
while True:
    _, frame = cap.read()
    roi = frame[180:440, 130:300]
    hsv_frame = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Blue
    low_blue = np.array([94, 80, 2])
    high_blue = np.array([126, 255, 255])
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
    blue = cv2.bitwise_and(roi, roi, mask=blue_mask)

    # Red
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    red = cv2.bitwise_and(roi, roi, mask=red_mask)

    # Green
    low_green = np.array([25, 52, 72])
    high_green = np.array([102, 255, 255])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    green = cv2.bitwise_and(roi, roi, mask=green_mask)

    # 3 Color detection
    # colorDetection = cv2.inRange(blue_mask, red_mask, green_mask)
    # Extract Region of interest
    detections = []
    # Object Detection
    contoursGreen, _ = cv2.findContours(
        green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contoursBlue, _ = cv2.findContours(
        blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contoursRed, _ = cv2.findContours(
        red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contoursGreen:
        # Calculate area and remove small element
        area = cv2.contourArea(cnt)
        if area > 850:
            # cv2.drawContours(roi, [cnt],-1,(0,255,0),2)
            x, y, w, h = cv2.boundingRect(cnt)
            detections.append([x, y, w, h])
            a = 2
            print(a)

    for cnt in contoursBlue:
        # Calculate area and remove small element
        area = cv2.contourArea(cnt)
        if area > 850:
            # cv2.drawContours(roi, [cnt],-1,(0,255,0),2)
            x, y, w, h = cv2.boundingRect(cnt)
            detections.append([x, y, w, h])
            a = 1
            print(a)

    for cnt in contoursRed:
        # Calculate area and remove small element
        area = cv2.contourArea(cnt)
        if area > 850:
            # cv2.drawContours(roi, [cnt],-1,(0,255,0),2)
            x, y, w, h = cv2.boundingRect(cnt)
            detections.append([x, y, w, h])
            a = 3
            print(a)
    
    # 2. Object Tracking
    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv2.putText(roi, str(id), (x, y),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv2.imshow("roi", roi)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(30)
    if key == 27:
        break

cap.realease()
cv2.destroyAllWindows()

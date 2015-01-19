import numpy as np
import cv2

cap = cv2.VideoCapture(0)

# take first frame of the video
ret,frame = cap.read()

drawing = np.zeros_like(frame)

state = 0 #0 do nothing, 1 draw, 2 erase
prevpoint = [];
currpoint = [];

# setup initial location of window
r,h,c,w = 200,40,500,40  # simply hardcoded the values
track_window = (c,r,w,h)

# set up the ROI for trackings
while(1):
    ret ,frame = cap.read()
    frame = cv2.flip(frame,1)
    roi2 = frame[r:r+h, c:c+w]
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    roi = hsv[r:r+h, c:c+w]

    cv2.rectangle(frame, (c,r), (c+w, r+h), (255,0,0))
    cv2.imshow('Put your color here!',frame)
    k = cv2.waitKey(10)
    if k ==ord('d'):
        cv2.destroyWindow('Put your color here!')
        break;

rgb = [0,0,0]
counter = 0

for row in roi2:
    for col in row:
        rgb[0] = rgb[0] + col[0]
        rgb[1] = rgb[1] + col[1]
        rgb[2] = rgb[2] + col[2]
        counter = counter + 1;

rgb[0] = rgb[0]/counter;
rgb[1] = rgb[1]/counter
rgb[2] = rgb[2]/counter

red = 0
green = 0
blue = 0
counter = 0

for row in roi:
    for col in row:
        red = red + col[0]
        green = green + col[1]
        blue = blue + col[2]
        counter = counter + 1;

red = red/counter;
green = green/counter
blue = blue/counter

MIN = np.array([red - 30,green - 30,blue - 30],np.uint8)
MAX = np.array([red + 30,green + 30,blue + 30],np.uint8)

while(1):
    ret ,frame = cap.read()
    frame = cv2.flip(frame,1)
    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        filtered = cv2.inRange(hsv,MIN,MAX)
        cv2.imshow("Tracker", filtered)

        moments = cv2.moments(filtered)
        if moments['m00']!=0:
            cx = int(moments['m10']/moments['m00']) # cx = M10/M00
            cy = int(moments['m01']/moments['m00'])
        else:
            cx = -1
            cy = -1

    currpoint = (int(cx),int(cy))
    if state == 1:
        if (prevpoint == []):
            cv2.circle(drawing, currpoint, 1, rgb, 2)
        else:
            cv2.line(drawing, prevpoint, currpoint, rgb, thickness=2,  lineType=8)
        prevpoint = currpoint
    elif state == 2:
        if (prevpoint == []):
            cv2.circle(drawing, currpoint, 1, (0,0,0), 2)
        else:
            cv2.line(drawing, prevpoint, currpoint, [0,0,0], thickness=10,  lineType=8)
        prevpoint = currpoint

    #add marker
    drawing2 = drawing.copy()
    cv2.line(drawing2, (int(cx - 5), int(cy)), (int(cx + 5), int(cy)), [0,0,255], thickness=1,  lineType=8)
    cv2.line(drawing2, (int(cx), int(cy-5)), (int(cx), int(cy+5)), [0,0,255], thickness=1,  lineType=8)
    cv2.imshow('Start drawing!',drawing2)

    k = cv2.waitKey(1)
    if k == ord('d'):
        if state == 0:
            state = 1
        else:
            state = 0
        prevpoint = []
    elif k == ord('r'):
        drawing = np.zeros_like(frame)
        drawing = frame  
        prevpoint = []
    elif k == ord('e'):
        if state == 2:
            state = 0
        else:
            state = 2
        prevpoint = []
    elif k == 27:
        break

cv2.destroyAllWindows()
cap.release()
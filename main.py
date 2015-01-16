import cv2
import numpy as np
cap = cv2.VideoCapture(0)
points = []
while(cap.isOpened()):
    ret, img = cap.read()
    # ret, img2 = cap.read()

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray,(5,5),0)
    # blur2 = cv2.GaussianBlur(gray,(5,5),0)

    ret, thresh1 = cv2.threshold(blur,200,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # ret, thresh2 = cv2.threshold(blur2,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    drawing = np.zeros(img.shape,np.uint8)

    contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    # import pdb
    # pdb.set_trace()

    # Draws the contours based off of area
    max_area=0
    for i in range(len(contours)):
        cnt=contours[i]
        area = cv2.contourArea(cnt)
        if(area>max_area):
            max_area=area
            ci=i
    cnt=contours[ci]
    hull = cv2.convexHull(cnt)

    # Finds the center of the image
    moments = cv2.moments(cnt)
    if moments['m00']!=0:
        cx = int(moments['m10']/moments['m00']) # cx = M10/M00
        cy = int(moments['m01']/moments['m00']) # cy = M01/M00

    # Provides us with the top of the convex hull
    max_hull = 10000
    hull_index = -1
    for i in xrange(len(hull)):
        if(hull[i][0][1] < max_hull):
            max_hull = hull[i][0][1]
            hull_index = i

    hull_center = (int(hull[hull_index][0][0]), int(hull[hull_index][0][1]))

    # Draws lines in between the tops of the finger
    points.append(hull_center)
    for idx, center in enumerate(points):
        if center == points[0]:
            cv2.circle(drawing, center, 1, (255,0,0), 2)
        else:
            other_center = points[idx-1]
            cv2.line(drawing, center, other_center, [255,0,0], thickness=1,  lineType=8)

    # Draws the contours and the circle 
    centr=(cx,cy)       
    cv2.circle(drawing,centr,5,[0,0,255],2)     
    cv2.drawContours(drawing,[cnt],0,(0,255,0),2) 
    cv2.drawContours(drawing,[hull],0,(0,0,255),2) 
          
    cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    hull = cv2.convexHull(cnt, returnPoints = False)
    
    # Detects defects. Need to do more research on understanding this
    if(1):
        defects = cv2.convexityDefects(cnt,hull)
        mind=0
        maxd=0
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])
            dist = cv2.pointPolygonTest(cnt,centr,True)
            cv2.line(img,start,end,[0,255,0],2)
                    
            cv2.circle(img,far,5,[0,0,255],-1)
            print(i)
            i=0
    cv2.imshow('output',drawing)
    # cv2.imshow('input',img)        
    k = cv2.waitKey(10)
    if k == 27:
        break
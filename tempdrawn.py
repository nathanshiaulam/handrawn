import numpy as np
import cv2
# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
def showVideo():
    points = []
    point_set = []
    erase_set = []

    draw = 0 
    erase = 0

    cap = cv2.VideoCapture(0)

    # take first frame of the video
    ret,frame = cap.read()
    # setup initial location of window
    r,h,c,w = 200,40,500,40  # simply hardcoded the values
    track_window = (c,r,w,h)

    # set up the ROI for trackings
    while(1):
        ret ,frame = cap.read()
        frame = cv2.flip(frame,1)
        roiRGB = frame[r:r+h, c:c+w]
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        roi = hsv[r:r+h, c:c+w]

        cv2.rectangle(frame, (c,r), (c+w, r+h), (255,0,0))
        cv2.imshow('Put your color here!',frame)
        k = cv2.waitKey(10)
        if k ==ord('d'):
            cv2.destroyWindow('Put your color here!')
            break;

    counter = 0;
    rgb = [0,0,0]

    for row in roiRGB:
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
    green = (green)/counter
    blue = blue/counter

    MIN = np.array([red - 30,green - 30,blue - 30],np.uint8)
    MAX = np.array([red + 30,green + 30,blue + 30],np.uint8)

    while(1):
        ret ,frame = cap.read()
        frame = cv2.flip(frame,1)
        if ret == True:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            filtered = cv2.inRange(hsv,MIN,MAX)
            cv2.imshow('Filtered!',filtered)
           
            moments = cv2.moments(filtered)
            if moments['m00']!=0:
                cx = int(moments['m10']/moments['m00']) # cx = M10/M00
                cy = int(moments['m01']/moments['m00'])

        drawing = frame;
        start = 0;
        if draw == 1:
            point_set.append((int(cx),int(cy)))
        else:
            point_set = []


        for idx, center in enumerate(point_set):
            if center == point_set[0]:
                cv2.circle(drawing, center, 1, rgb, 2)
                marker = 0
            else:
                other_center = point_set[idx-1]
                cv2.line(drawing, center, other_center, rgb, thickness=2,  lineType=8)
                print str([red, green, blue])


        for set_of_points in points:
            for idx, center in enumerate(set_of_points):
                if center == set_of_points[0]:
                    cv2.circle(drawing, center, 1, rgb, 2)
                    marker = 0
                else:
                    other_center = set_of_points[idx-1]
                    cv2.line(drawing, center, other_center, rgb, thickness=2,  lineType=8)

        

        cv2.imshow('Start drawing!',drawing)

        k = cv2.waitKey(1)
        if k == ord('d'):
            if draw == 0:
                draw = 1
                erase = 0
            else:
                draw = 0
                points.append(point_set)
        elif k == ord('r'):
            points = []
        elif k == 27:
            break

    cv2.destroyAllWindows()
    cap.release()

showVideo()
# if __name__ == "__main__":
#     app.run()
#!/usr/bin/env python3
#
# Demonstrates streaming and modifying the image via Opencv2
#    hue = [12, 95]
 #   sat = [100, 255]
  #  val = [32, 255]


import cscore as cs
import numpy as np
import cv2
from networktables import NetworkTables
import argparse
import os
from goalpipeline import *




def main():
    SCALE=2
    WIDTH=160*SCALE
    HEIGHT=90*SCALE
    FPS=15
    hue = [77,90]
    sat = [73,255]
    val = [188, 255]

    #blur_type = BlurType.Box_Blur
    blur_radius = 17
    blur_ksize = int(1 * round(blur_radius) + 1)
    #powercell = powercellcv()
    camera = cs.UsbCamera("usbcam", 0)
    camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, WIDTH, HEIGHT, FPS)

   # mjpegServer = cs.MjpegServer("httpserver", 8081)
   # mjpegServer.setSource(camera)

   # print("mjpg server listening at http://0.0.0.0:8081")

    cvsink = cs.CvSink("cvsink")
    cvsink.setSource(camera)

    cvSource = cs.CvSource("cvsource", cs.VideoMode.PixelFormat.kMJPEG, WIDTH, HEIGHT, FPS)
    cvMjpegServer = cs.MjpegServer("PowerCell", 8081)
    cvMjpegServer.setSource(cvSource)

    print("OpenCV output mjpg server listening at http://0.0.0.0:8081")

    test = np.zeros(shape=(HEIGHT, WIDTH, 3), dtype=np.uint8)
    flip = np.zeros(shape=(HEIGHT, WIDTH, 3), dtype=np.uint8)
    #out = self.hsv_threshold_output
    kernel = None
    anchor = (-1, -1)
    iterations = 1.0
    bordertype = cv2.BORDER_CONSTANT
    bordervalue = (-1)
    

    #=====
    NetworkTables.initialize(server='roborio-5607-frc.local')
    sd = NetworkTables.getTable("goal")
    goal = GoalPipeline()
  # cs2 = cs2.getInstance()
  # cs2.enableLogging()

  # camera2 = cs2.startAutomaticCapture()

  # camera2.setResolution(320, 240)

  # # Get a CvSink. This will capture images from the camera
  # cvSink2 = cs2.getVideo()

  # # (optional) Setup a CvSource. This will send images back to the Dashboard
  # outputStream2 = cs2.putVideo("Rectangle", 320, 240)

  # # Allocating new images is very expensive, always try to preallocate
  # img2 = np.zeros(shape=(240, 320, 3), dtype=np.uint8)

  # while True:
  #     # Tell the CvSink to grab a frame from the camera and put it
  #     # in the source image.  If there is an error notify the output.
  #     time, img = cvSink.grabFrame(img)

    while True:

        time, frame = cvsink.grabFrame(test)
        if time == 0:
            print("error:", cvsink.getError())
            continue
        goal.process(frame)
        cnts = goal.filter_contours_output
        #print("got frame at time", time, test.shape)

        #cv2.flip(test, flipCode=0, dst=flip)
        #filename=os.path.join("./capture2."+str(time)+".jpg")
        #cv2.imwrite(filename, frame)
        #out = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
        #out = cv2.blur(out,(blur_ksize, blur_ksize))
        #out = cv2.inRange(out, (hue[0], sat[0], val[0]),  (hue[1], sat[1], val[1]))
        #out = cv2.dilate(out, kernel, anchor, iterations = 0)#, cv2.BORDER_CONSTANT , bordervalue)
        #out = cv2.erode(out, kernel, anchor, iterations = 0)#, cv2.BORDER_CONSTANT , bordervalue)
        #cnts, a = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        center = None
        boundRect=None



        #only do stuff if a single contor was found
        if len(cnts) > 0:
            #find the largest contour in the mask, then use it
            #to compute the minimum enclosing circle and centroid
            c = max(cnts, key=cv2.contourArea)
            ((x,y), radius) = cv2.minEnclosingCircle(c)
            boundRect = cv2.boundingRect(c)
            M = cv2.moments(c)
            try:
                center = (int(M["m10"] / M["m00"]), int (M["m01"] / M["m00"]))
            except ZeroDivisionError:
                pass


            #if the dectected contour has a radius big enough, we will send it
            if radius > 0:
                #draw a circle around the target and publish values to smart dashboard
                cv2.circle(frame, (int(x), int(y)), int(radius), (255,255,8), 2)
                cv2.circle(frame, center, 3, (0,0,225), -1)
                cv2.rectangle(frame, (int(boundRect[0]), int(boundRect[1])), \
                   (int(boundRect[0]+boundRect[2]), int(boundRect[1]+boundRect[3])), (0,0,225), 2)
                ###Starting to draw the rectangle
               # threshold = val
    #
               # canny_output = cv2.Canny(src_gray, threshold, threshold * 2)
    #
    #
               # _, contours, _ = cv2.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #
    #
               # contours_poly = [None]*len(contours)
               # boundRect = [None]*len(contours)
               # centers = [None]*len(contours)
               # radius = [None]*len(contours)
               # for i, c in enumerate(contours):
               #     contours_poly[i] = cv2.approxPolyDP(c, 3, True)
               #     boundRect[i] = cv2.boundingRect(contours_poly[i])
               #     centers[i], radius[i] = cv2.minEnclosingCircle(contours_poly[i])
    #
    #
               # drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    #
    #
               # for i in range(len(contours)):
               #     color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
               #     cv2.drawContours(drawing, contours_poly, i, color)
               #     cv2.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), \
               #         (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)
               #     cv2.circle(drawing, (int(centers[i][0]), int(centers[i][1])), int(radius[i]), color, 2)
    
    
                sd.putNumber('X',x)
                sd.putNumber('Y',y)
                sd.putNumber('R', radius)
                #print("X: " + repr(round(x, 1)) + " Y: " + repr(round(y, 1)) + " Radius: " + repr(round(radius, 1)))

            else:
                #print("Nothing seen")
                #let the RoboRio Know no target has been detected with -1
                sd.putNumber('X', -1)
                sd.putNumber('Y', -1)
                sd.putNumber('R', -1)

        #powercell.process(test)
        cvSource.putFrame(frame)
      
    
#cv2.imshow('Contours', drawing)
#parser = argparse.ArgumentParser(description='Code for Creating Bounding boxes and circles for contours tutorial.')
#parser.add_argument('--input', help='Path to input image.', default='stuff.jpg')
#args = parser.parse_args()
#src = cv2.imread(cv.samples.findFile(args.input))
#if src is None:
#    print('Could not open or find the image:', args.input)
#    exit(0)
# Convert image to gray and blur it
#src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
#src_gray = cv2.blur(src_gray, (3,3))
#source_window = 'Source'
#cv2.namedWindow(source_window)
#cv2.imshow(source_window, src)
#max_thresh = 255
#thresh = 100 # initial threshold
#cv2.createTrackbar('Canny thresh:', source_window, thresh, max_thresh, thresh_callback)
#thresh_callback(thresh)
#cv2.waitKey()


if __name__ == "__main__":
    main()



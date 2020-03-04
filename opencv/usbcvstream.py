#!/usr/bin/env python3
#
# Demonstrates streaming and modifying the image via OpenCV
#    hue = [12, 95]
 #   sat = [100, 255]
  #  val = [32, 255]


import cscore as cs
import numpy as np
import cv2
from powercellcv import *
from networktables import NetworkTables

def main():
    SCALE=2
    WIDTH=160*SCALE
    HEIGHT=90*SCALE
    FPS=15
    hue = [9.712230215827338, 57.82664451107176]
    sat = [159.60172539934155, 255.0]
    val = [128.6331951388042, 255.0]
    blur_type = BlurType.Box_Blur
    blur_radius = 4.716981132075472
    blur_ksize = int(2 * round(blur_radius) + 1)
    powercell = powercellcv()
    camera = cs.UsbCamera("usbcam", 1)
    camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, WIDTH, HEIGHT, FPS)

   # mjpegServer = cs.MjpegServer("httpserver", 8081)
   # mjpegServer.setSource(camera)

   # print("mjpg server listening at http://0.0.0.0:8081")

    cvsink = cs.CvSink("cvsink")
    cvsink.setSource(camera)

    cvSource = cs.CvSource("cvsource", cs.VideoMode.PixelFormat.kMJPEG, WIDTH, HEIGHT, FPS)
    cvMjpegServer = cs.MjpegServer("Goal", 8082)
    cvMjpegServer.setSource(cvSource)

    print("OpenCV output mjpg server listening at http://0.0.0.0:8082")

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
    sd = NetworkTables.getTable("powerball")
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

        #print("got frame at time", time, test.shape)

        #cv2.flip(test, flipCode=0, dst=flip)
        out = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        out = cv2.blur(out,(blur_ksize, blur_ksize))
        out = cv2.inRange(out, (hue[0], sat[0], val[0]),  (hue[1], sat[1], val[1]))
        out = cv2.dilate(out, kernel, anchor, iterations = 3)#, cv2.BORDER_CONSTANT , bordervalue)
        out = cv2.erode(out, kernel, anchor, iterations = 2)#, cv2.BORDER_CONSTANT , bordervalue)
        cnts, a = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        center = None



        #only do stuff if a single contor was found
        if len(cnts) > 0:
            #find the largest contour in the mask, then use it
            #to compute the minimum enclosing circle and centroid
            c = max(cnts, key=cv2.contourArea)
            ((x,y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            try:
                center = (int(M["m10"] / M["m00"]), int (M["m01"] / M["m00"]))
            except ZeroDivisionError:
                pass


            #if the dectected contour has a radius big enough, we will send it
            if radius > 7:
                #draw a circle around the target and publish values to smart dashboard
                cv2.circle(frame, (int(x), int(y)), int(radius), (255,255,8), 2)
                cv2.circle(frame, center, 3, (0,0,225), -1)
                sd.putNumber('X',x)
                sd.putNumber('Y',y)
                sd.putNumber('R', radius)
                #print("X: " + repr(round(x, 1)) + " Y: " + repr(round(y, 1)) + " Radius: " + repr(round(radius, 1)))

            else:
                #print("WTF")
                #let the RoboRio Know no target has been detected with -1
                sd.putNumber('X', -1)
                sd.putNumber('Y', -1)
                sd.putNumber('R', -1)

        #powercell.process(test)
        cvSource.putFrame(frame)
      


if __name__ == "__main__":
    main()



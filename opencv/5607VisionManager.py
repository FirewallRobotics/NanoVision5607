'''
 MIT License
 
 Copyright (c) 2023
 
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
 
 FRC Team Firewall 5607
 - File: 5607VisionManager.py 
 
 - CurrentYear:  2023
 - CreationDay: 5 
 - Date: Fri Mar 17 2023 
 - Username: wendydarby
 '''
 
#import apriltag
import argparse
import cv2 
import numpy as np
from networktables import NetworkTables
import sys
import cscore as cs
import team5607NetworkTables
import coneVision
import cubeVision

import time as t
import glob
''' The prupose of the Vision Mange is to provide a frame work for the vision scripts
    This class manages the connections to the cameras aso that thre wont be any conflicts 
    and developer can unit test on local laptop, jetson or pi.

    This allows team to focus on vision image processing in sub classes and not have to
    worry about how to connect to the camera

    Vision Sub Classes should have a process function that takes an image as an argument and 
    a modified image or data about the image.
'''

def connectCameraServerCamera():
  #TODO function needs testing on Jetson
    #Using WPILIb CameraServer implementation
  '''cameras = {
          "apriltag": "/dev/v4l/by-id/usb-EMEET_HD_Webcam_eMeet_C960_SN0001-video-index0",
          "items": "/dev/v4l/by-id/usb-Microsoft_Microsoft®_LifeCam_HD-3000-video-index0"
      }
    camera = cs.UsbCamera("usbcam", cameras["apriltag"])#1, devcam or vid'''
  '''vid = cv2.VideoCapture(0)
  cs = CameraServer
  cs.enableLogging()
  # cs.UsbCamera("usbcam", "0")
  camera = cs.startAutomaticCapture()
  cvsink = cs.getVideo()'''

  '''When CameraServer opens a camera, it creates a webpage that you can use to view the camera 
  stream and view the effects of various camera settings. To connect to the web interface, use 
  a web browser to navigate to http://roborio-5607-frc.local:1181. '''
  #init the CameraServer
  camServ = cs.CameraServer

  camServ.enableLogging()

  camera1 = camServ.startAutomaticCapture()
  #server = camServ.getServer()
  #cscore is agressive in turning off camras not in use, need to do this when we have multiple cameras to keep them on.
  #camera1.setConnectionStrategy(VideoSource.ConnectionStrategy.kKeepOpen)
  print("Setting source for camera1")
  #server.setSource(camera1)

  windowWidth = 640
  windowHeight = 480
  brightness = 100
  FPS=30

  #Setup output to dashboard
  output = cs.CameraServer.putVideo("DriveCam", windowWidth, windowHeight)
  camera1.setResolution(windowWidth, windowHeight)
  #camera1.setVideoMode(VideoMode.PixelFormat.kMJPEG, windowWidth, windowHeight, FPS)
  # Allocating new images is very expensive, always try to preallocate
  # shape tuple is rows, columns, so I'm assuming we should allocate same as window size
  img = np.zeros(shape=(windowHeight, windowWidth, 3), dtype=np.uint8)
  #cvsink = cs.CameraServer.getVideo()
  #cvsink.setSource(camera1)
  #camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, WIDTH, HEIGHT, FPS)

  cvsink = cs.CvSink("cvsink")
  cvSource = cs.CvSource("DriveCam", cs.VideoMode.PixelFormat.kMJPEG, windowWidth, windowHeight, FPS) #get rid of red by nanovision code
  
  while True:
      # Tell the CvSink to grab a frame from the camera and put it
      # in the source image. If there is an error notify the output. time, img = cvSink.grabFrame(img)
      time, img = cvsink.grabFrame(img)
      #ret, img = camera1.grabFrame(img)
      if time == 0:
        # Send the output the error.
        # skip the rest of the current iteration continuep
        output.notifyError(cvsink.getError())
        print("time waas 0")
        continue
      #
      # Insert your image processing logic here!
      #
      # (optional) send some image back to the dashboard
      output.putFrame(img)
       
          
      cvSource.putFrame(img)
      cv2.imwrite("/home/root/UsbStick/"+ str(number) + "drivesample.png", img) #comment out later
      
      t.sleep(15) #15 seconds of sleep
      number += 1

    
    

def connectOpencvCamera():
    #function for connecting to local laptop camera

    #Setup camera connection
    windowWidth = 640
    windowHeight = 480
    brightness = 100
    FPS=30

    #Setup output to dashboard
    output = cs.CameraServer.putVideo("April Tag Vision Name", windowWidth, windowHeight)
    #camera1.setResolution(windowWidth, windowHeight)
    #camera1.setVideoMode(VideoMode.PixelFormat.kMJPEG, windowWidth, windowHeight, FPS)
    # Allocating new images is very expensive, always try to preallocate
    # shape tuple is rows, columns, so I'm assuming we should allocate same as window size
    img = np.zeros(shape=(windowHeight, windowWidth, 3), dtype=np.uint8)
    #cvsink = cs.CameraServer.getVideo()
    #cvsink.setSource(camera1)
    #camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, WIDTH, HEIGHT, FPS)

    
 
    #Using the local laptop webcam and openCV
    vid =cv2.VideoCapture(0)
    if not vid.isOpened():
      print("Cannot open camera")
      exit()

    #get first frame
    ret, img = vid.read()

    #Dislay camera feed in local window
    i=1
    while (i<6):   
      ret, img = vid.read()
      print("read from camera again ")
      print(i)
      if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
    
      i+=1
      cv2.imshow('img', img)
      # (optional) send some image back to the dashboard using wplilib CameraServer impl


      #TODO test vision processing here

      #Send processed image to Smartboard
      output.putFrame(img)
      image_copy= cubeVision.localCubeVision(img)
      #cvsink = cs.CvSink("cvsink")
      
      #Make it easy to close the camera display window, just press q to close window
      if cv2.waitKey(0) == ord('q'):
        continue
  
    # When everything done, release the capture
    vid.release()
    cv2.destroyAllWindows()


# call script with "local" to use openCV camera connection 
# no argument to script will default to CameraServer UsbCamera
if __name__ == '__main__':
  #intitialize Vision Network Tables 
  #in competeion it is recommended to use static ip's 10.56.07.2 would be out team's static ip.
  team5607_vision=team5607NetworkTables.visionTable(server='roborio-5607-frc.local', tableName="apriltag")
  
  if len(sys.argv)<2:
    print("Defaulting to CameraServer implementation")    
    connectCameraServerCamera()
  elif sys.argv[1].lower() == 'local':
    print("Connecting to local Camera with OpenCV")
    connectOpencvCamera()
  
  
  sys.exit()

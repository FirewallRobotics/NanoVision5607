import cv2
import numpy as np
from networktables import NetworkTables
import cscore as cs
#ßimport cubevisiongrip
from cubevisiongrip import Cube
 
 def cubeProcess(frame, hue, sat, val):
            ''' Adds the filters to the image
            
            args:
            frame - 
            hue - The hue of the cube.
            sat - The saturation of the cube.
            val - The value of the cube.
            
            returns:
            '''
  
        kernel = None
        anchor = (-1, -1)
        borderValue = (-1)
        out = cv2.inRange(frame, (hue[0], sat[0], val[0]), (hue[1], sat[1], val[1]) #threshold
        out = cv2.erode(out, kernel, anchor, iterations = 7.5, borderType = cv2.BORDER_CONSTANT, borderValue) #erode
        out = cv2.dilate(out, kernel, anchor, iterations = 17, borderType = cv2.BORDER_CONSTANT, borderValue) #dilate
        cents, a = cv2.findContours(out, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #Finding Contours
        
        center = [0,0]
        data = [[0,0], 0]
          # only if a single contor was founded.
        if len(cnts) > 0:
             # find the largest contour then use it.
             # to compute the minimum enclosing circle and centroid.
          c = max(cnts, key = cv2.contourArea)
          ((x,y)), radius) = cv2.minEnclosingCircle(c)
          M = cv2.moments(c)
          try:  
                center = (int(M["m10"] / M["m00"], int (M["m01"] / M["m00"]))
                data = [center, radius]

          except ZeroDivisionError:
              center = [0,0]
              data = [center, 0]
                          
def drawCircle(frame, center, radius, color, minRadius = 7):
    '''
    frame = image
    center = (x,y)
    radius = int
    color = (R,G,B)
    
    '''
    if radius > minRadius:
                          
                          #draw a circle around the target and publish values to smart dashboard
       cv2.circle(frame, center, int(radius), color, 2)### change here color is a R
       #print(f'{center}, r:{radius}')
    return frame
       

SCALE=1
WIDTH=160*SCALE
HEIGHT=90*SCALE
FPS=15

test = np.zeros(shape=(HEIGHT, WIDTH, 3), dtype=np.uint8)

cameras = {
        "apriltag": "/dev/v4l/by-id/usb-EMEET_HD_Webcam_eMeet_C960_SN0001-video-index0",
        "items": "/dev/v4l/by-id/usb-Microsoft_Microsoft®_LifeCam_HD-3000-video-index0"
    }
camera = cs.UsbCamera("usbcam", cameras["items"])#1, devcam or vid
camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, WIDTH, HEIGHT, FPS)

cvsink = cs.CvSink("cvsink")
cvsink.setSource(camera)

cvSource = cs.CvSource("cvsource", cs.VideoMode.PixelFormat.kMJPEG, WIDTH, HEIGHT, FPS) #get rid of red by nanovision code
cvSourceMid = cs.CvSource("cvsource", cs.VideoMode.PixelFormat.kMJPEG, WIDTH, HEIGHT, FPS) #get rid of red by nanovision code

cvMjpegServer = cs.MjpegServer("cube", 5802)#here
cvMjpegServer.setSource(cvSource)
cvMjpegServerMid = cs.MjpegServer("cubePipeline`", 8082)#here #not too sure
cvMjpegServerMid.setSource(cvSourceMid)
count = 0


cubeimage = Cube()

while True:
    count += 1
    time, imageorg = cvsink.grabFrame(test)
    if time == 0:
        print("error:", cvsink.getError())

        continue
    image_pipeline = cubeimage.process(imageorg)
    cvSourceMid.putFrame(image_pipeline)
    contours = cubeimage.findContours()
    # draw contours on the original image + dilate the image
    image_copy = imageorg.copy()
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    NetworkTables.initialize(server='roborio-5607-frc.local')##change to be the IP adress of computer
    # mrPhilips laptop # NetworkTables.initialize(server='192.168.1.64')##change to be the IP adress of computer
    try:
        biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
        x,y,w,h = cv2.boundingRect(biggest_contour)
        print(f'{x}, {y}, {x+w}, {y+h}')
        image_copy = cv2.rectangle(image_copy, (x,y),(x+w,y+h), color=(0, 255, 0))
        sd1 = NetworkTables.getTable("cone")
        sd1.putNumber('x_min', x)  ## tuple
        sd1.putNumber('y_min', y) #tuple
        sd1.putNumber('x_max',x+w)
        sd1.putNumber('y_max',y+h)

    except ValueError:
        pass


    cvSource.putFrame(image_copy)

import cv2
import numpy as np
from networktables import NetworkTables
import cscore as cs
#ßimport cubevisiongrip
from cubevisiongrip import Cube
import time as t
 
def cubeProcess(frame, hue, sat, val):
    ''' Adds the filters to the image
            
    args:
        frame - 
        hue - The hue of the cube.
        sat - The saturation of the cube.
        val - The value of the cube.
          
        returns:
         data - The list of the filters
    '''
  
    kernel = None
    anchor = (-1, -1)
    borderValue = (-1)
    out = cv2.inRange(frame, (hue[0], sat[0], val[0]), (hue[1], sat[1], val[1])) #threshold
    out = cv2.erode(out, kernel, anchor, iterations = 3, borderType = cv2.BORDER_CONSTANT, borderValue = borderValue) #erode
    out = cv2.dilate(out, kernel, anchor, iterations = 14, borderType = cv2.BORDER_CONSTANT, borderValue = borderValue) #dilate
    cnts, a = cv2.findContours(out, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #Finding Contours
    
    center = [0,0]
    data = [[0,0], 0]
    # only if a single contor was founded.
    if len(cnts) > 0:
    # find the largest contour then use it.
    # to compute the minimum enclosing circle and centroid.
        c = max(cnts, key = cv2.contourArea)
        ((x,y)), radius = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        try:  
            center = (int(M["m10"] / M["m00"]), int (M["m01"] / M["m00"]))
            data = [center, radius]
        except ZeroDivisionError:
            center = [0,0]
            data = [center, 0]
    data.append(out)
    return data
                          
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
    
def localCubeVision(imageorg):
    cubeimage = Cube()

    hue = [107.56656740921443, 171.19016287354705]
    sat = [83.95683599032944, 255.0]
    val = [97.8417240672832, 255.0]
    color = (0, 0, 225) #RGB
    number = 1
    
    cubeimage.process(imageorg)
    

    contours = cubeimage.find_contours_output
    
    # draw contours on the original image + dilate the image
    image_copy = imageorg.copy()
    cubeData= cubeProcess(imageorg, hue, sat,val)
    
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    
    cubeimage.process(imageorg)
    contours = cubeimage.find_contours_output
    # draw contours on the original image + dilate the image
    image_copy = imageorg.copy()
    cubeData= cubeProcess(imageorg, hue, sat,val)
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
  ##change to be the IP adress of computer
    # mrPhilips laptop # NetworkTables.initialize(server='192.168.1.64')##change to be the IP adress of computer
    try:
        data = cubeProcess(imageorg, hue, sat, val)
        center = data[0]
        radius = data[1]
        #image = data[2]
        sd1 = NetworkTables.getTable("cube")
        sd1.putNumber("Center", str(center))  ## tuple
        sd1.putNumber("Raidus", radius) #tuple


    except ValueError:
        pass


    if number == 4:
    
    ##change to be the IP adress of computer
    # mrPhilips laptop # NetworkTables.initialize(server='192.168.1.64')##change to be the IP adress of computer
   
    
        
    

 #   cvSource.putFrame(image_copy)
        cv2.imwrite(str(number) + "conesample.png", image_copy) #comment out later
        cv2.imwrite(str(number) + "coneproc.png", image_copy) #comment out later
        t.sleep(15) #15 seconds of sleep
        return image_copy



if __name__ == "__main__":

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



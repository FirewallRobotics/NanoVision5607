
import cv2
import numpy as np
from networktables import NetworkTables
import cscore as cs
#ßimport conevisiongrip
from conevisiongrip import Cone


SCALE=1
WIDTH=160*SCALE
HEIGHT=90*SCALE
FPS=15

test = np.zeros(shape=(HEIGHT, WIDTH, 3), dtype=np.uint8)

cameras = {
        "apriltag": "/dev/v4l/by-id/usb-EMEET_HD_Webcam_eMeet_C960_SN0001-video-index0",
        "microsoft_powerpoints": "/dev/v4l/by-id/usb-Microsoft_Microsoft®_LifeCam_HD-3000-video-index0"
    }
camera = cs.UsbCamera("usbcam", cameras["cone"])#1, devcam or vid
camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, WIDTH, HEIGHT, FPS)

cvsink = cs.CvSink("cvsink")
cvsink.setSource(camera)

cvSource = cs.CvSource("cvsource", cs.VideoMode.PixelFormat.kMJPEG, WIDTH, HEIGHT, FPS) #get rid of red by nanovision code
cvSourceMid = cs.CvSource("cvsource", cs.VideoMode.PixelFormat.kMJPEG, WIDTH, HEIGHT, FPS) #get rid of red by nanovision code

cvMjpegServer = cs.MjpegServer("cone", 5802)#here
cvMjpegServer.setSource(cvSource)
cvMjpegServerMid = cs.MjpegServer("conePipeline`", 8082)#here #not too sure
cvMjpegServerMid.setSource(cvSourceMid)
count = 0


coneimage = Cone()

while True:
    count += 1
    time, imageorg = cvsink.grabFrame(test)
    if time == 0:
        print("error:", cvsink.getError())

        continue
    image_pipeline = coneimage.process(imageorg)
    cvSourceMid.putFrame(image_pipeline)
    contours = coneimage.findContours()
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

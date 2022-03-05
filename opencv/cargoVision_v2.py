#!/usr/bin/env python3

import cscore as cs
import numpy as np
import cv2
from networktables import NetworkTables

def preprocess(frame,blur_radius=10):

    out = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    return blurImage(out,blur_radius)

def cargoProcess(frame, hue, sat, val):
    kernel = None
    anchor = (-1, -1)
    out = cv2.inRange(frame, (hue[0], sat[0], val[0]),  (hue[1], sat[1], val[1]))
    #out = cv2.erode(frame, kernel, anchor, iterations = 2)
    #out = cv2.dilate(out, kernel, anchor, iterations = 3)#, cv2.BORDER_CONSTANT , bordervalue)########
    #out = cv2.erode(out, kernel, anchor, iterations = 2)#, cv2.BORDER_CONSTANT , bordervalue)

    cnts, a = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    center = [0,0]
    data = [ [0,0], 0]
    #only do stuff if a single contor was found
    if len(cnts) > 0:
        #find the largest contour in the mask, then use it
        #to compute the minimum enclosing circle and centroid
        c = max(cnts, key=cv2.contourArea)
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        ## v wouldn't run after the return?
        try:
            center = (int(M["m10"] / M["m00"]), int (M["m01"] / M["m00"]))
            data = [center, radius]

        except ZeroDivisionError:
            center = [0,0]
            data = [center, 0]
        
    data.append(out)   
    return data
        
class _team5607_NetworkTables:
    def __init__(self, server="roborio-5607-frc.local", tableName="cargo", tableKeys=[]):
        self.server=server
        self.tableName=tableName
        NetworkTables.initialize(server)
        self.sd = NetworkTables.getTable(self.tableName)
        self.tableKeys=tableKeys
        # Initialize each key in the table with a -1
        self.tableKV={key: -1 for key in self.tableKeys}
        self.updateTable(self.tableKV)
    def updateTable(self,tableKV):
        for key in tableKV:
            self.tableKV[key] = tableKV[key]
            self.sd.putNumber(f'{key}',tableKV[key])


def setupSinkSource(devID, sourceLable, sourcePort, WIDTH, HEIGHT, FPS):
    camera = cs.UsbCamera("usbcam", devID)
    camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, WIDTH, HEIGHT, FPS)

    cvsink = cs.CvSink("cvsink")
    cvsink.setSource(camera)

    cvSource = cs.CvSource("cvsource", cs.VideoMode.PixelFormat.kMJPEG, WIDTH, HEIGHT, FPS)
    cvMjpegServer = cs.MjpegServer(sourceLable, sourcePort)
    print(f'OpenCV output mjpg server listening at http://team5607.local:{sourcePort}')
    cvMjpegServer.setSource(cvSource)
    return cvsink, cvSource

def blurImage(image, blur_radius=10):
    blur_ksize = int(2 * round(blur_radius) + 1)
    return cv2.blur(image,(blur_ksize, blur_ksize))

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

    return frame



def main():
    SCALE=2
    WIDTH=160*SCALE
    HEIGHT=90*SCALE
    # 160x90 is the smallest, we can use SCALE to pick larger sizes
    FPS=15
    ##cvsink, cvSource = setupSinkSource(0,"Cargo", 8082, WIDTH, HEIGHT, FPS)
    camera = cs.UsbCamera("usbcam", 0)#1, devcam or vid
    camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, WIDTH, HEIGHT, FPS)

    cvsink = cs.CvSink("cvsink")
    cvsink.setSource(camera)

    cvSource = cs.CvSource("cvsource", cs.VideoMode.PixelFormat.kMJPEG, WIDTH, HEIGHT, FPS) #get rid of red by nanovision code
    cvSourceMid = cs.CvSource("cvsource", cs.VideoMode.PixelFormat.kMJPEG, WIDTH, HEIGHT, FPS) #get rid of red by nanovision code

    cvMjpegServerMid = cs.MjpegServer("PowerCell", 8082)#here
    cvMjpegServerMid.setSource(cvSourceMid)

    cvMjpegServer = cs.MjpegServer("PowerCell", 8081)#here
    cvMjpegServer.setSource(cvSource)
    cargo={
      "blue": {
          "hue": [92, 110],
          "sat": [108, 230],
          "val": [48, 255],
          "color": (255,0,0) # RGB
      },
        "red":  {
            "hue":  [147, 180],
            "sat": [113, 230.0],
            "val": [175, 255.0],
            "color": (0,0,255) # RGB
        }
    }

 
    # For each cargo we are going to need to create an x,y,r piece of data
    cargoData=["X_", "Y_", "R_"]
    # This is nested list comprehension.  Intent is to get X|Y|R_{label}
    # Below results in ['X_blue', 'Y_blue', 'R_blue', 'X_red', 'Y_red', 'R_red']
    tableKeys=[data + label for label in cargo.keys() for data in cargoData]
    # Move network tables complexity to a single call
    team5607_cargo=_team5607_NetworkTables(server='roborio-5607-frc.local', tableName="cargo", tableKeys=tableKeys)
    # Start capturing video
    count = 0
    while True:
        time, frame = cvsink.grabFrame(np.zeros(shape=(HEIGHT, WIDTH, 3), dtype=np.uint8))
        if time == 0:
            print("error:", cvsink.getError())
            continue
        count+=1
        image=frame.copy()
        image=preprocess(image)
        if count == 10:
            cv2.imwrite('source.jpg', frame)
        
        for label in cargo.keys():
                # We only want to get the x,y,r based on a clean preprocessed image ONLY.
                data = cargoProcess(image, hue=cargo[label]["hue"],sat=cargo[label]["sat"],val=cargo[label]["val"])
                centers = data[0]
                rad = data[1]
                # Now draw circles on the original image
                frame = drawCircle(frame, centers, rad, color=cargo[label]["color"], minRadius = 7)
                team5607_cargo.updateTable({f"X_{label}":centers[0], f"Y_{label}":centers[1], f"R_{label}":rad})

        cvSource.putFrame(frame)


if __name__ == "__main__":
    main()



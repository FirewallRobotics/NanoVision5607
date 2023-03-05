import apriltag
import argparse
import cv2 
import numpy as np
from networktables import NetworkTables
import sys
from cscore import CameraServer
# import AprilTagPoseEstimator
#import Transform3d
#import Rotation3d
import glob
'''
def area(ptA, ptB, ptC, ptD):
  """Finds the area of the apriltag.
  args:
    ptA, ptB, ptC, ptD - the corners of the shape
  returns:
    area - Area of the shape
    by timmy :)
  """
  length = ptB[0] - ptA[0]
  width = ptB[1] - ptC[1]
  area = length * width
  return area'''
  
# construct the argument parser and parse the arguments
#def main():
####thinking here
#Setup camera connection
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

#Using the local laptop webcam and openCV
windowWidth = 640
windowHeight = 840
brightness = 100

#Setup output to dashboard
cs = CameraServer
output = cs.putVideo("Name", windowWidth, windowHeight)

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
  
  #Darby camera is dark let's adjust the contrast and birghtness
  '''# define the contrast and brightness value
  contrast = 5. # Contrast control ( 0 to 127)
  brightness = 2. # Brightness control (0-100)

  # call addWeighted function. use beta = 0 to effectively only operate on one image
  out = cv2.addWeighted( img, contrast, img, 0, brightness)'''

  i+=1
  cv2.imshow('img', img)
  # (optional) send some image back to the dashboard using wplilib CameraServer impl
  output.putFrame(img)
  #Make it easy to close the cmera display window, just press q to close window
  if cv2.waitKey(0) == ord('q'):
    continue
  
# When everything done, release the capture
vid.release()
cv2.destroyAllWindows()
sys.exit()
# (optional) Setup a CvSource. This will send images back to the Dashboard
#outputStream = cs.putVideo("Name", 320, 240)
'''
# camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, WIDTH, HEIGHT, FPS)
# Allocating new images is very expensive, always try to preallocate
img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)
while True:
    # Tell the CvSink to grab a frame from the camera and put it
    # in the source image. If there is an error notify the output. time, img = cvSink.grabFrame(img)
    time, img = cvsink.grabFrame(img)
    if time == 0:
        # Send the output the error.
      # skip the rest of the current iteration continue
      #outputStream.notifyError(cvsink.getError())
    #
    # Insert your image processing logic here!
    #
    # (optional) send some image back to the dashboard
outputStream.putFrame(img)
cvsink = cs.CvSink(ImageSink(VideoSink.kMjpeg),VideoSink())
cvsink.setSource(camera)

cvSource = cs.CvSource("cvsource", cs.VideoMode.PixelFormat.kMJPEG, WIDTH, HEIGHT, FPS) #get rid of red by nanovision code
cvSourceMid = cs.CvSource("cvsource", cs.VideoMode.PixelFormat.kMJPEG, WIDTH, HEIGHT, FPS) #get rid of red by nanovision code

cvMjpegServer = cs.MjpegServer("apriltag", 5802)#here
cvMjpegServer.setSource(cvSource)
cvMjpegServerMid = cs.MjpegServer("conePipeline`", 8082)#here #not too sure
cvMjpegServerMid.setSource(cvSourceMid)

###end of thinking


###Implimentation of Camera Calibration code
chessboardSize = (24,17)
frameSize = (1440,1080)



# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)


# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

size_of_chessboard_squares_mm = 20
objp = objp * size_of_chessboard_squares_mm


# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

### End of Abby's implimentation
### Start of Timm and James implimentation (Check at some point)
images = glob.glob('*.png')

for image in images:
  img = cv2.imread(image)
  gray = cv2.cvtColor(img, cv.COLOR_BGR2GRAY)
  
  #Find the chess board corners
  ret, corners = cv2.findChessboardCorners(gray, chessboardSize, None)
  
  if ret == True:
    objpoints.append(objp)
    corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
    # Draw and display the corners
    cv2.drawChessboardCorners(img, chessboardSize, corners2, ret)
    cv2.imshow('img',img)
    cv2.waitKey(1000)
    
cv2.destroyAllWindows()

############## CALIBRATION #######################################################

ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, frameSize, None, None)

############## UNDISTORTION ######################################################

img = cv2.imread('cali5.png')
h, w = img.shape[:2]
newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))

# Undistort
dst = cv2.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv2.imwrite('caliResult2.png', dst)
                   
# Reprojection Error
mean_error = 0
                   
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    mean_error += error

print( "total error: {}".format(mean_error/len(objpoints)) )

############ End of the edit, you can fix whatever we messed up #################################
                   
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
  help="path to input image containing AprilTag")
args = vars(ap.parse_args())
 
 # load the input image and convert it to grayscale
print("[INFO] loading image...")
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
 # define the AprilTags detector options and then detect the AprilTags
 # in the input image
print("[INFO] detecting AprilTags...")
options = apriltag.DetectorOptions(families="tag16h5")
detector = apriltag.Detector(options)
results = detector.detect(gray)
print("[INFO] {} total AprilTags detected".format(len(results)))
       
##poseEstConfig = AprilTagPoseEstimator.Config(0,0,0,0,0) #need numbers
#e#stimator = AprilTagPoseEstimator(poseEstConfig)
 
 # loop over the AprilTag detection results
for r in results:
  # extract the bounding box (x, y)-coordinates for the AprilTag
  # and convert each of the (x, y)-coordinate pairs to integers
  (ptA, ptB, ptC, ptD) = r.corners
  ptB = (int(ptB[0]), int (ptB[1]))
  ptC = (int(ptC[0]), int (ptC[1]))
  ptD = (int(ptD[0]), int (ptD[1]))
  ptA = (int(ptA[0]), int (ptA[1]))
  
  
  # draw the bounding box of the AprilTag detection
  cv2.line(image, ptA, ptB, (0, 255, 0), 2)
  cv2.line(image, ptB, ptC, (0, 255, 0), 2)
  cv2.line(image, ptC, ptD, (0, 255, 0), 2)
  cv2.line(image, ptD, ptA, (0, 255, 0), 2)
  
  # draw the center (x, y)-coordinates of the AprilTag
  (cX, cY) = (int(r.center[0]), int(r.center[1]))
  cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)
  ID = r.tag_id
           
  # draw the tag family on the image
  tagFamily = r.tag_family.decode("utf-8")
  cv2.putText(image, tagFamily, (ptA[0], ptA[1] - 15),
    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
  print("[INFO] tag family: {}".format(tagFamily))
  
  pose = estimator.estimate(r)
  rot = pose.getRotation()
   
           
# show the output image after AprilTag detection
NetworkTables.initialize(server='roborio-5607-frc.local')
sd1 = NetworkTables.getTable("apriltag")
sd1.putNumber('Point A', ptA)  ## tuple
sd1.putNumber('Point B', ptB) #tuple
sd1.putNumber('Point C', ptC)
sd1.putNumber('Point D', ptD)
sd1.putNumber('Center X', cX)
sd1.putNumber('Center Y', cY)
sd1.putNumber('ID', ID)'''

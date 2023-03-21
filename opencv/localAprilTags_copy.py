import apriltag
import argparse
import cv2 
import numpy as np
from networktables import NetworkTables, NetworkTablesInstance
import sys
#from cscore import CameraServer, VideoSource, VideoMode, VideoSink, CvSink, CvSource
import cscore as cs
import team5607NetworkTables
import coneVision

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

def connectCameraServerCamera():
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

  camera1 = camServ.startAutomaticCapture(0)
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
  output = cs.CameraServer.putVideo("Name", windowWidth, windowHeight)
  camera1.setResolution(windowWidth, windowHeight)
  #camera1.setVideoMode(VideoMode.PixelFormat.kMJPEG, windowWidth, windowHeight, FPS)
  # Allocating new images is very expensive, always try to preallocate
  # shape tuple is rows, columns, so I'm assuming we should allocate same as window size
  img = np.zeros(shape=(windowHeight, windowWidth, 3), dtype=np.uint8)
  #cvsink = cs.CameraServer.getVideo()
  #cvsink.setSource(camera1)
  #camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, WIDTH, HEIGHT, FPS)

  #cvsink = cs.CvSink("cvsink")
  cvSource = cs.CvSource("aprilTags Camera", cs.VideoMode.PixelFormat.kMJPEG, windowWidth, windowHeight, FPS) #get rid of red by nanovision code
  '''
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

    '''
    

def connectOpencvCamera(visionNt):
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

    iCamState=visionNt.getEntry("/Transitory Values/Item Cam Status")
    iCamState.setString("Intializing...")
    #Using the local laptop webcam and openCV
    vid =cv2.VideoCapture(0)
    if not vid.isOpened():
      print("Cannot open camera")
      iCamState.setString("not connected")
      exit()

    robotState= ntinst.getEntry("/RobotState")
    print("The robot state is: "+robotState.getString("unset"))
    print("item camera state is: "+iCamState.getString("unset"))
    #get first frame
    ret, img = vid.read()

    #Dislay camera feed in local window
    i=1
    while (i<6):   
      ret, img = vid.read()
      print("read from camera again ")
      robotState= ntinst.getEntry("/RobotState")
      print("The robot state is: "+robotState.getString("unset"))
      print("item camera state is: "+iCamState.getString("unset"))
      print(i)
      if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
      '''
        #Darby camera is dark let's adjust the contrast and birghtness
        # define the contrast and brightness value
        contrast = 5. # Contrast control ( 0 to 127)
        brightness = 2. # Brightness control (0-100)

        # call addWeighted function. use beta = 0 to effectively only operate on one image
        out = cv2.addWeighted( img, contrast, img, 0, brightness)
      '''

      i+=1
      cv2.imshow('img', img)
      # (optional) send some image back to the dashboard using wplilib CameraServer impl
      output.putFrame(img)
      iCamState.setString("posting image")
      coneVision.localConeVision(img)
     

      cvSource = cs.CvSource("aprilTags Camera", cs.VideoMode.PixelFormat.kMJPEG, windowWidth, windowHeight, FPS) #get rid of red by nanovision code
      cvsink = cs.CvSink("cvsink")
      cvsink.setSource(cvSource)

      '''cvSource = cs.CvSource("aprilTags Camera", cs.VideoMode.PixelFormat.kMJPEG, windowWidth, windowHeight, FPS) #get rid of red by nanovision code

      cvMjpegServer = cs.MjpegServer("aprilTaags", port=5801)#here
      cvMjpegServer.setSource(cvSource)
      # mjpg:http://<IP or host>:<port>/?action=stream
      csTable = NetworkTables.getDefault()
      csTable.getEntry("/CameraPublisher/PiCam/streams").setStringArray(["mjpeg:http://127.0.0.1:5801/?action=stream"])
      '''
      #Make it easy to close the camera display window, just press q to close window
      if cv2.waitKey(0) == ord('q'):
        continue
  
    # When everything done, release the capture
    vid.release()
    cv2.destroyAllWindows()
'''


# (optional) Setup a CvSource. This will send images back to the Dashboard
#outputStream = cs.putVideo("Name", 320, 240)

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

# construct the argument parser and parse the arguments
#def main():

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
'''
'''
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


# call script with "local" to use openCV camera connection 
# no argument to script will default to CameraServer UsbCamera
if __name__ == '__main__':
  #intitialize Vision Network Tables 
  #in competeion it is recommended to use static ip's 10.56.07.2 would be out team's static ip.
  #team5607_visionNT=team5607NetworkTables.visionTable(server='127.0.0.1', tableName="apriltag")
  NetworkTables.initialize('127.0.0.1')
  NT_DEFAULT_PORT=1735
  ntinst = NetworkTablesInstance.getDefault()
  ntinst.startClientTeam(5607, NT_DEFAULT_PORT)
  
  robotState= ntinst.getEntry("/RobotState")
  print("The robot state is: "+robotState.getString("unset"))
  if len(sys.argv)<2:
    print("Defaulting to CameraServer implementation")    
    connectCameraServerCamera()
  elif sys.argv[1].lower() == 'local':
    print("Connecting to local Camera with OpenCV")
    connectOpencvCamera(NetworkTables)
  
  sys.exit()

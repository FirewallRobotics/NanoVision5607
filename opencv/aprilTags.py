import apriltag
import argparse
import cv2
from networktables import NetworkTables
import AprilTagPoseEstimator
import Transform3d
import Rotation3d
import glob

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
  return area
  
# construct the argument parser and parse the arguments

####thinking here
cameras = {
        "cone": "/dev/v4l/by-id/usb-EMEET_HD_Webcam_eMeet_C960_SN0001-video-index0",
        "cargo": "/dev/v4l/by-id/usb-Microsoft_Microsoft®_LifeCam_HD-3000-video-index0"
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
  img = cv.imread(image)
  gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
  
  #Find the chess board corners
  ret, corners = cv.findChessboardCorners(gray, chessboardSize, None)
  
  if ret == True:
    objpoints.append(objp)
    corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
    # Draw and display the corners
    cv.drawChessboardCorners(img, chessboardSize, corners2, ret)
    cv.imshow('img',img)
    cv.waitKey(1000)
    
cv.destroyAllWindows()

############## CALIBRATION #######################################################

ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, frameSize, None, None)

############## UNDISTORTION ######################################################

img = cv.imread('cali5.png')
h, w = img.shape[:2]
newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))

# Undistort
dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix

# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv.imwrite('caliResult2.png', dst)
                   
# Reprojection Error
mean_error = 0
                   
for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
    mean_error += error

print( "total error: {}".format(mean_error/len(objpoints)) )

############ End of the edit, you can fix whatever we messed up #################################
                   
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
  help="path to input image containing AprilTag")
 args = vars(ap.parse_args())
 
 # load the input image and convert it to grayscale
 print("[INFO] loading image..."
 image = cv2.imread(args["image"])
 gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
 # define the AprilTags detector options and then detect the AprilTags
 # in the input image
 print("[INFO] detecting AprilTags...")
 options = apriltag.DetectorOptions(families="tag16h5")
 detector = apriltag.Detector(options)
 results = detector.detect(gray)
 print("[INFO] {} total AprilTags detected".format(len(results)))
       
poseEstConfig = AprilTagPoseEstimator.Config(0,0,0,0,0) #need numbers
estimator = AprilTagPoseEstimator(poseEstConfig)
 
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
  cv2.line(image, ptA, ptB, [0, 255, 0), 2]
  cv2.line(image, ptB, ptC, [0, 255, 0), 2]
  cv2.line(image, ptC, ptD, [0, 255, 0), 2]
  cv2.line(image, ptD, ptA, [0, 255, 0), 2]
  
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
 sd1.putNumber('ID', ID)

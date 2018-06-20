from pyimagesearch.shapedetector import ShapeDetector
from pyimagesearch.colorlabeler import ColorLabeler
import imutils
import socket
import urllib
import cv2
import argparse



ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())
image = cv2.imread(args["image"])
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])

      # convert the resized image to grayscale, blur it slightly,
      # and threshold it
blurred = cv2.GaussianBlur(resized, (5, 5), 0)
gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB)
thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
      #
  # find contours in the thresholded image and initialize the
  # shape detector
cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
sd = ShapeDetector()
cl = ColorLabeler()

  # loop over the contours
for c in cnts:
    # compute the center of the contour, then detect the name of the
    # shape using only the contour
         M = cv2.moments(c)
         cX = int((M["m10"] / M["m00"]) * ratio)
         cY = int((M["m01"] / M["m00"]) * ratio)
         shape = sd.detect(c)
         color = cl.label(image, c)
    
    # multiply the contour (x, y)-coordinates by the resize ratio,
    # then draw the contours and the name of the shape on the image
         c = c.astype("float")
         c *= ratio
         c = c.astype("int")
         text = "{} {}".format(color, shape)
         cv2.drawContours(image, [c], -1, (255, 255, 255), 3)
         cv2.putText(image, text, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # show the output image
         cv2.imshow("Image", image)
         cv2.waitKey(0)



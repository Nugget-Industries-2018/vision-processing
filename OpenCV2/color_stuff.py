from pyimagesearch.shapedetector import ShapeDetector
import cv2
import numpy as np
import imutils
from matplotlib import pyplot as plt

# Capture the input frame from webcam
def get_frame(cap, scaling_factor):
    # Capture the frame from video capture object
    ret, frame = cap.read()

    # Resize the input frame
    frame = cv2.resize(frame, None, fx=scaling_factor,
            fy=scaling_factor, interpolation=cv2.INTER_AREA)

    return frame

if __name__=='__main__':

    #uncomment whichever camera you'd like to use (0 is first webcam it detects)
    #cap = cv2.VideoCapture('http://10.0.0.234:8082/?action=stream')
    cap = cv2.VideoCapture(0)
    scaling_factor = 0.5
    color = "unidentified"
    plane = "Unidentified Aircraft"

    # Iterate until the user presses ESC key
    while True:
        i = 0
        frame = get_frame(cap, scaling_factor)

        # Convert the HSV colorspace
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        print hsv
        # Define 'blue' range in HSV colorspace and its mask
        lower_blue = np.array([110,50,50])
        upper_blue = np.array([130,255,255])
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Define 'yellow' range in HSV colorspace and its mask
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])
        yellow_mask  = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Define 'red' range in HSV colorspace and its mask
        lower_red = np.array([0,50,50])
        upper_red = np.array([10,255,255])
        red_mask = cv2.inRange(hsv, lower_red, upper_red)

        # Threshold the HSV image to only detect blue, red, and yellow
        mask = red_mask

        # Sets the color variable equal to whatever mask it detects
        if np.array_equal(mask, blue_mask):
            color = "blue"

        elif np.array_equal(mask, red_mask):
            color = "red"

        elif np.array_equal(mask, yellow_mask):
            color = "yellow"

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame, frame, mask=mask)
        res = cv2.medianBlur(res,5)
        # Pre-process image to optimize shape detection
        resized = imutils.resize(res, width=910)
        ratio = frame.shape[0] / float(resized.shape[0])
        blurred = cv2.GaussianBlur(res, (5, 5), 0)
        gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
        lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
              #
          # find contours in the thresholded image and initialize the
          # shape detector
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        sd = ShapeDetector()


          # loop over the contours
        for c in cnts:
            # compute the center of the contour, then detect the name of the
            # shape using only the contour
                 M = cv2.moments(c)
            #Adds 1 to the denominator to prevent division by 0
                 cX = int((M["m10"] / (M["m00"]+1)) * ratio)
                 cY = int((M["m01"] / (M["m00"]+1)) * ratio)

            # multiply the contour (x, y)-coordinates by the resize ratio,
            # then draw the contours and the name of the shape on the image
                 c = c.astype("float")
                 c *= ratio
                 c = c.astype("int")
                 shape = sd.detect(c)

            #Translates corresponding shape and color to the designated Aircraft
                 if (color == "red" and shape == "triangle"):
                    plane = "Aircraft A"

                 if (color == "yellow" and shape == "triangle"):
                    plane = "Aircraft B"

                 if (color == "blue" and shape == "triangle"):
                    plane = "Aircraft C"

                 if (color == "red" and shape == "rectangle"):
                    plane = "Aircraft D"

                 if (color == "yellow" and shape == "rectangle"):
                    plane = "Aircraft E"

                 if (color == "blue" and shape == "rectangle"):
                    plane = "Aircraft F"

            #Formats the text and overlays it on the live feed
                 text = "{} {} {}".format(color, shape, plane)
                 cv2.putText(frame, text, (80, 126), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        cv2.imshow('Original image', frame)
        cv2.imshow('Color Detector', res)


        # Check if the user pressed ESC key, if yes terminates window
        c = cv2.waitKey(5)
        if c == 27:
            break

    cv2.destroyAllWindows()

from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2

import io
import os


# Instantiates a client

vidcap = cv2.VideoCapture('videos/line1_Trim.mp4')
success,image = vidcap.read()
success = True
pathOut = "imgs/"
count = 0
while success:
    success,image = vidcap.read()
    if count % 10 == 0:
        cv2.imwrite( pathOut + "\\frame%d.jpg" % (count/10), image)     # save frame as JPEG file
    count += 1

count = int(count/10) #total number of frames


# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# loop over the image paths
for i in range (count-1):
	current_xs = []
	future_xs = []
	imagePath = "imgs/frame{}.jpg".format(i)
	futurePath = "imgs/frame{}.jpg".format((i+1))

	# load the image and resize it to (1) reduce detection time
	# and (2) improve detection accuracy
	image = cv2.imread(imagePath)
	future_image = cv2.imread(futurePath)

	image = imutils.resize(image, width=min(400, image.shape[1]))
	orig = image.copy()
	future_image = imutils.resize(future_image, width=min(400, future_image.shape[1]))

	# detect people in the image
	(rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
	    padding=(8, 8), scale=1.05)

	(f_rects, f_weights) = hog.detectMultiScale(future_image, winStride=(4, 4),
	    padding=(8, 8), scale=1.05)

	# draw the original bounding boxes
	for (x, y, w, h) in rects:
	    cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)

	# apply non-maxima suppression to the bounding boxes using a
	# fairly large overlap threshold to try to maintain overlapping
	# boxes that are still people
	rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
	f_rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in f_rects])

	pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
	f_pick = non_max_suppression(f_rects, probs=None, overlapThresh=0.65)

	# draw the final bounding boxes
	for (xA, yA, xB, yB) in pick:
		cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
		current_xs.append(xA)
	
	for (fx, fy, fw, fh) in f_pick:
	    cv2.rectangle(image, (fx, fy), (fw, fh), (255, 0, 0), 1)
	    future_xs.append(fx)

	#direction = calculate_direction(current_xs, future_xs)


	# show some information on the number of bounding boxes
	filename = imagePath[imagePath.rfind("/") + 1:]
	print("[INFO] {}: {} original boxes, {} after suppression".format(
	    filename, len(rects), len(pick)))

	# show the output images
	cv2.imshow("Before NMS", orig)
	cv2.imshow("After NMS", image)
	cv2.waitKey(4)
	cv2.imwrite("draw/draw{}.jpg".format(i), image)


def calculate_direction(current_xs, future_xs):
	current_xs = current_xs.sort()
	future_xs = current_xs.sort()

	#takes in current x positions and future x positions

	#determines line, whether standing still or moving, start and end of line
	if len(current_xs) > len(future_xs):
		diff = len(current_xs) - len(future_xs)
		counter = 0;
		for i in range(len(future_xs)):
			if diff > 0 and abs(current_xs[i] - future_xs[i]) > 40:
				del current_xs[i]
				diff = diff - 1;
	elif len(current_xs) < len(future_xs):
		diff = len(future_xs) - len(current_xs)
		counter = 0
		for i in range(len(future_xs)):
			if diff > 0 and abs(current_xs[i] - future_xs[i]) > 40:
				del future_xs[i]
				diff = diff - 1;

	diff = []
	num_left = 0
	num_right = 0
	num_still = 0
	for i in range(len(future_xs)): #still = 1
		diff.append(future_xs[i] - current_xs[i])
		if future_xs[i] - current_xs[i] < -10:
			num_left += 1
		elif future_xs[i] - current_xs[i] > 10:
			num_right += 1
		else:
			num_still += 1

	direction = ""
	if (num_left >= num_right) and (num_left >= num_still):
	   direction = "left"
	elif (num_right >= num_left) and (num_right >= num_still):
	   direction = "right"
	else:
	   direction = "still"

	return direction
	








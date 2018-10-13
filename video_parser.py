import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
import PIL.Image

# for drawing boxes
from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2


# Instantiates a client
client = vision.ImageAnnotatorClient()

import cv2
vidcap = cv2.VideoCapture('videos/line1_Trim.mp4')
success,image = vidcap.read()
success = True
pathOut = "imgs/"
count = 0
'''while success:
    success,image = vidcap.read()
    if count % 30 == 0:
        cv2.imwrite( pathOut + "\\frame%d.jpg" % (count/30), image)     # save frame as JPEG file
    count += 1'''

count = 29 #total number of frames

for num_frame in range(count):
    filename = "imgs/frame{}.jpg".format(num_frame)
    with io.open(filename, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    teams = []
    for label in labels:
        if label.name == 'team':
            teams.append(label)
            print(label.bounding_poly)

    im = PIL.Image.open(filename)
    draw = ImageDraw.Draw(im)

    for team in teams:
        box = [(vertex.x, vertex.y)
               for vertex in team.bounding_poly.vertices]
        draw.line(box + [box[0]], width=5, fill='#ffffff')

    im.save("draw/draw{}.jpg".format(num_frame))

    # Performs label detection on the image file
    '''
    '''

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# loop over the image paths
for i in range (29):
    imagePath = "imgs/frame{}.jpg".format(i)
    # load the image and resize it to (1) reduce detection time
    # and (2) improve detection accuracy
    image = cv2.imread(imagePath)
    image = imutils.resize(image, width=min(400, image.shape[1]))
    orig = image.copy()

    # detect people in the image
    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
        padding=(8, 8), scale=1.05)

    # draw the original bounding boxes
    for (x, y, w, h) in rects:
        cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # apply non-maxima suppression to the bounding boxes using a
    # fairly large overlap threshold to try to maintain overlapping
    # boxes that are still people
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    # draw the final bounding boxes
    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

    # show some information on the number of bounding boxes
    filename = imagePath[imagePath.rfind("/") + 1:]
    print("[INFO] {}: {} original boxes, {} after suppression".format(
        filename, len(rects), len(pick)))

    # show the output images
    cv2.imshow("Before NMS", orig)
    cv2.imshow("After NMS", image)
    cv2.waitKey(1)


    
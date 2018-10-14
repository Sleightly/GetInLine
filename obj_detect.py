from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import io
import cv2
import statistics
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
import PIL.Image

def localize_objects(count,name):
    client = vision.ImageAnnotatorClient()
    
    for i in range (count):
        filename = "imgs/{}/frame{}.jpg".format(name, i)
        with io.open(filename, 'rb') as image_file:
            content = image_file.read()        
        image = types.Image(content=content)
        objects = client.object_localization(
            image=image).localized_object_annotations

        im = PIL.Image.open(filename)
        draw = ImageDraw.Draw(im)
        width, height = im.size

        print('Number of objects found: {}'.format(len(objects)))
        for object_ in objects:
            #print('\n{} (confidence: {})'.format(object_.name, object_.score))
            #print('Normalized bounding polygon vertices: ')
            #for vertex in object_.bounding_poly.normalized_vertices:
            #    print(' - ({}, {})'.format(vertex.x, vertex.y))
            box = [(vertex.x * width, vertex.y * height) for vertex in object_.bounding_poly.normalized_vertices]
            draw.line(box + [box[0]], width=5, fill='#00ff00')

        im.save("draw/{}/draw{}.jpg".format(name, i))

def print_photos(count, name):
    for i in range (count):
        imagePath = "draw/{}/draw{}.jpg".format(name, i)
        cv2.imshow("After", cv2.imread(imagePath))
        cv2.waitKey(50)


def count_imgs(file, name):
    print("parsing video\n")
    vidcap = cv2.VideoCapture(file)
    success,image = vidcap.read()
    success = True
    pathOut = "imgs/{}/".format(name)
    count = 0
    while success:
        success,image = vidcap.read()
        if count % 10 == 0:
            cv2.imwrite( pathOut + "\\frame%d.jpg" % (count/10), image)     # save frame as JPEG file
        count += 1
    count = int(count/10)
    print("finished parsing video\n")
    return count

def resize_imgs(count, name):
    for i in range (count):
        path = "resize/{}/res{}.jpg".format(name, i)
        filename = "imgs/{}/frame{}.jpg".format(name, i)
        image = cv2.imread(filename)
        r = 400.0 / image.shape[1]
        dim = (400, int(image.shape[0] * r))
        resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        cv2.imshow("resized", resized)
        cv2.waitKey(50)
        cv2.imwrite(path, resized)

def cross_correlation(count, name):
    #split resize image into fourths
    magnitude = []
    for i in range(count-1):
        path = "resize/{}/res{}.jpg".format(name, i)
        f_path = "resize/{}/res{}.jpg".format(name, i+1)

        image = cv2.imread(path)
        gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        height, width = gray_scale.shape[:2]

        #crop 4 images
        start_row, start_col = int(0), int(0)
        end_row, end_col = height, int(width * .05)
        width_offset = int(width * .05)
        max_width = width - width_offset

        cropped = []
        indices = []
        for i in range(20):
            cropped.append(gray_scale[start_row:end_row, start_col:end_col].ravel())
            indices.append(start_col)
            start_row, start_col = 0, end_col
            end_row, end_col = height, (end_col+width_offset)
        
        #compare to future image
        f_image = cv2.imread(f_path)
        f_gray_scale = cv2.cvtColor(f_image, cv2.COLOR_BGR2GRAY)

        #calculate offset based on maximum of dot product
        #print("calculating offset")
        offset = [0]*20

        for i in range(len(cropped)):
            start_row, start_col = int(0), int(0)
            end_row, end_col = height, width_offset
            max_val = 0
            offset_index = 0
            for j in range(max_width):
                f_cropped = f_gray_scale[start_row:end_row, start_col:end_col].ravel()

                test_value = np.dot(cropped[i], f_cropped)
                if (test_value > max_val):
                    max_val = test_value
                    offset_index = j

                start_row, start_col = 0, start_col+1
                end_row, end_col = height, end_col+1

            offset[i] = offset_index

        #print(offset)
        #print(indices)

        # normalize offset
        normalized = []
        for i in range(len(offset)):
            normalized.append(offset[i] - indices[i])
        
        #median of array
        #magnitude of line
        #print(statistics.median(normalized))
        magnitude.append(statistics.median(normalized))
        
        #print(statistics.mean(normalized))
        #print()
    print(magnitude)
    return magnitude


if __name__ == '__main__':
    name = 'line3'
    #count = count_imgs('videos/line3.mp4', name)
    count = 302
    #print("resizing")
    #resize_imgs(count, name)
    #print("cross correlation")
    #cross_correlation(count, name)
    #print('drawing boxes')
    #localize_objects(count, name)
    print("printing photos")
    print_photos(count, name)
   



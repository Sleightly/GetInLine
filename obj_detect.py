import io
import cv2
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
import PIL.Image

def localize_objects():
    client = vision.ImageAnnotatorClient()
    count = 100
    
    for i in range (count):
        filename = "imgs/frame{}.jpg".format(i)
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
            for vertex in object_.bounding_poly.normalized_vertices:
                print(' - ({}, {})'.format(vertex.x, vertex.y))
            box = [(vertex.x * width, vertex.y * height) for vertex in object_.bounding_poly.normalized_vertices]
            draw.line(box + [box[0]], width=5, fill='#00ff00')

        im.save("draw/draw{}.jpg".format(i))

localize_objects()

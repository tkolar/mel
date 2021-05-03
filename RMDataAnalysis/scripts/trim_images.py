import sys
import os
import csv
import datetime
import json
from bokeh.plotting import figure, show
import numpy as np
# import necessary libraries

import cv2
import numpy as np
import pprint


from rmd_common import rmd_get_items
from rmd_common import rmd_get_isbns

DATA_DIR = "/Users/tkolar/mel/spines/"
SECTION = "F"

ROTATION_INCREMENT = 5
LINEAR_INCREMENT = 100
MAX_SPINE_WIDTH = 1000

WHITE = (255, 255, 255)

items = rmd_get_items()
isbns = rmd_get_isbns()

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR, borderValue=WHITE)
  return result

#
# change the perspective so that (hopefully) the sides of the book are parallel
#
def transform_image(image):
    SQUEEZE = 100
    # Locate points of the documents or object which you want to transform
    pts1 = np.float32([[0, 0], [1500, 0], [SQUEEZE, 4100], [1500-SQUEEZE, 4100]])
    pts2 = np.float32([[0, 0], [1500, 0], [0, 4100], [1500, 4100]])

    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(image, matrix, (1500, 4100))
    # Wrap the transformed image
    return(result)

def histogram_compare(book_image, black_image):

    bgr_planes1 = cv2.split(black_image)
    bgr_planes2 = cv2.split(book_image)
    histSize = 256
    histRange = (0, 256)
    accumulate = False

    b1_hist = cv2.calcHist(bgr_planes1, [0], None, [histSize], histRange, accumulate=accumulate)
    g1_hist = cv2.calcHist(bgr_planes1, [1], None, [histSize], histRange, accumulate=accumulate)
    r1_hist = cv2.calcHist(bgr_planes1, [2], None, [histSize], histRange, accumulate=accumulate)

    b2_hist = cv2.calcHist(bgr_planes2, [0], None, [histSize], histRange, accumulate=accumulate)
    g2_hist = cv2.calcHist(bgr_planes2, [1], None, [histSize], histRange, accumulate=accumulate)
    r2_hist = cv2.calcHist(bgr_planes2, [2], None, [histSize], histRange, accumulate=accumulate)

    b_comp = cv2.compareHist(b1_hist, b2_hist, 0) * 100
    g_comp = cv2.compareHist(g1_hist, g2_hist, 0) * 100
    r_comp = cv2.compareHist(r1_hist, r2_hist, 0) * 100
    average = (b_comp + g_comp + r_comp)/3
    return(average)


def estimate_width(barcode):
    item = items[barcode]
    isbn_number = item["ISBN"]
    isbn = isbns[isbn_number]
    #if "number_of_pages" in isbn:
    #    width_estimate = int(isbn["number_of_pages"]) 
    #         * page_size for paperback or hardback
    return(300)

def main():

    pp = pprint.PrettyPrinter(indent=4)

    file = open(DATA_DIR + "conn-F.json")
    connections = json.load(file)

    black_img = cv2.imread("black_bar.png", cv2.IMREAD_COLOR)

    is_first_sample = True
    first_sample = None

    keys = list(connections.keys())

    for barcode in keys:
        width_estimate = estimate_width(barcode)
        image_name = connections[barcode] 
        img_raw = cv2.imread(DATA_DIR + SECTION + "-trimmed" + "/" + image_name, cv2.IMREAD_COLOR)

        img = transform_image(img_raw)

        x_middle= int(img.shape[1] / 2)
        x_offset= x_middle + 100
        y_offset=1700

        black_width = black_img.shape[0]
        black_height = black_img.shape[1]

        rotated_images = []

        for r in range(-30,30+ROTATION_INCREMENT,ROTATION_INCREMENT):
            r_img = rotate_image(img.copy(), r)
            rotated_images.append((r, r_img))

        best_score = -10.0
        best = (0.0, 0, 0, None) # score, angle, offset from middle, rotated_img
        scan_zone = range(x_offset, x_offset + int(MAX_SPINE_WIDTH/2), LINEAR_INCREMENT)

        for i in scan_zone:
            for (angle, rotated_image) in rotated_images:
                #  
                # img sample is the same size  as the black bar
                #
                img_sample = rotated_image[y_offset:y_offset+black_width, i:i+black_height] 
                hist_score = histogram_compare(img_sample, black_img)

                #
                # check for new high score
                #
                if hist_score > best_score:
                    best = (hist_score, angle, i, rotated_image)
                    best_score = hist_score
                    print(best_score)
                    print("best angle:", angle)

                visible_img = rotated_image.copy()
                visible_img[y_offset:y_offset+black_width, i:i+black_height] = black_img
                #cv2.imshow("Vertical",visible_img)
                #c = cv2.waitKey(0)
                #if c == ord('q'):
                #    sys.exit(0)
                #if c == ord('n'):
                #    break


        (score, angle, x_offset, best_img) = best
        #best_img[y_offset:y_offset+width, x_offset:x_offset+height] = black_img
        FRAME_TOP = 800
        offset_from_middle = x_offset - x_middle

        left = x_middle - int(offset_from_middle * .6666)
        right = x_offset
        top = FRAME_TOP 
        bottom = FRAME_TOP + 3000 

        print(angle)
        best_img = rotate_image(best_img, 0-angle)
        cv2.rectangle(best_img, (left, top), (right, bottom), WHITE, 12)

        cv2.imshow("Vertical",best_img)

        c = cv2.waitKey(0)
        if c == ord('q'):
            sys.exit(0)
        if c == ord('n'):
            break

main()


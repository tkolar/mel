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

items = rmd_get_items()
isbns = rmd_get_isbns()

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
    print(book_image.shape, black_image.shape)

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
    print("b:%.2f  g:%.2f  R:%.2f" % (b_comp, g_comp, r_comp))
    return(0)


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

    for barcode in connections:
        width_estimate = estimate_width(barcode)
        image_name = connections[barcode] 
        img_raw = cv2.imread(DATA_DIR + SECTION + "-trimmed" + "/" + image_name, cv2.IMREAD_COLOR)

        img = transform_image(img_raw)

        x_offset= 1000
        x_offset= int(img.shape[1] / 2)
        y_offset=1700

        width = black_img.shape[0]
        height = black_img.shape[1]


        while(True):
            img_copy = img.copy()  # don't touch the original

            #  
            # img sample is the same size  as the black bar
            #
            img_sample = img_copy[y_offset:y_offset+width, x_offset:x_offset+height] 
            histogram_compare(img_sample, black_img)

            #
            # Place the black bar on the image
            #
            img_copy[y_offset:y_offset+width, x_offset:x_offset+height] = black_img

            cv2.imshow("Vertical",img_copy)

            c = cv2.waitKey(0)
            if c == ord('q'):
                sys.exit(0)
            if c == ord('n'):
                break
            if c == ord(' '):
                x_offset += 20

        
main()


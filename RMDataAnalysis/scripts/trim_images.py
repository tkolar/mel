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

    black_img = cv2.imread("black_bar.png", 0)

    for barcode in connections:
        width_estimate = estimate_width(barcode)
        image_name = connections[barcode] 
        img = cv2.imread(DATA_DIR + SECTION + "-trimmed" + "/" + image_name, 0)

        x_offset= 1000
        x_offset= int(img.shape[1] / 2)
        print(x_offset)
        y_offset=1700

        while(True):
            width = black_img.shape[0]
            height = black_img.shape[1]
            img_copy = img.copy()
            img_copy[y_offset:y_offset+width, x_offset:x_offset+height] = black_img
            cv2.imshow("Vertical",img_copy)

            c = cv2.waitKey(0)
            if c == ord('q'):
                sys.exit(0)
            if c == ord('n'):
                break
            if c == ord(' '):
                x_offset += 100

        
main()


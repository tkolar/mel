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


from rmd_common import rmd_get_items
from rmd_common import rmd_get_isbns

DATA_DIR = "/Users/tkolar/mel/spines/"

SECTION = "F"
BARCODE_FILENAME = DATA_DIR + "all-" + SECTION + ".txt"
CONNECTIONS_FILENAME = DATA_DIR + "conn-" + SECTION + ".json"

isbns = rmd_get_isbns()
items = rmd_get_items()

def valid_isbn(barcode):

    if barcode not in items:
        return(False)

    item_isbn = items[barcode]["ISBN"]

    if item_isbn not in isbns:
        return(False)

    isbn = isbns[item_isbn]
    return(True)

def main():

    conn_file = open(CONNECTIONS_FILENAME)
    conns = json.load(conn_file)
    conn_file.close()


    bookinfo = {}

    file_contents = open(BARCODE_FILENAME).read()
    barcodes = file_contents.split("\n")
    barcodes = barcodes[0:-1]   # chop off the (blank) last entry
    for i in range(0, len(barcodes)):
        barcodes[i] = barcodes[i].lstrip("0")

    image_names = os.listdir(DATA_DIR + SECTION + "-trimmed")
    image_names.sort()

    if "cursor" in conns:
        image_index, barcode_index = conns["cursor"]
    else:
        image_index = 0
        barcode_index = 0
    while(True):
        if image_index >= len(image_names):
            conn_file = open(CONNECTIONS_FILENAME, "w")
            conns["cursor"] = (image_index, barcode_index)
            json.dump(conns, conn_file)
            sys.exit(0)

        image_name = image_names[image_index]
        num_potentials = min(9, len(barcodes) - barcode_index)
        start = max(0, barcode_index - 5)
        potential_barcodes = barcodes[start:start + num_potentials + 1]
        for i,barcode in enumerate(potential_barcodes):
            if barcode not in items:
                continue
            print(i, items[barcode]["Title"])

        img = cv2.imread(DATA_DIR + SECTION + "-trimmed" + "/" + image_name, 0)
        rotated_img = cv2.rotate(img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)

        cv2.imshow("Vertical",img)
        cv2.imshow("Horizontal",rotated_img)

        chosen_index = -1
        while(True):
            c = cv2.waitKey(0)

            if c == 13:
                c = '0'

            if c == ord('q'):
                conn_file = open(CONNECTIONS_FILENAME, "w")
                conns["cursor"] = (image_index, barcode_index)
                json.dump(conns, conn_file)
                sys.exit(0)
            elif c == ord('s'):
                print("Skipped")
                barcode_index -= 1
                break
            elif (chr(c) >= '0') and (chr(c) <= '9'):
                chosen_index = int(chr(c))
                print(chosen_index)
                barcode = potential_barcodes[chosen_index]
                conns[barcode] = image_name
                break
            elif c == 2:   # left arrow
                print("Left arrow!")
                barcode_index -= 3
                image_index -= 3
                break;

            else:
                print("Invalid input decimal %03d" % c)

        # skip up to the next barcode with an isbn
        barcode_index += 1
        while not valid_isbn(barcodes[barcode_index]):
            barcode_index += 1

        image_index += 1

        #print ("\n" * 100)
        print ("\n" * 3)
        
main()


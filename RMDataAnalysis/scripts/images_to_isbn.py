import sys
import os
import csv
import datetime
from bokeh.plotting import figure, show
import numpy as np
# import necessary libraries

import cv2
import numpy as np


from rmd_common import rmd_get_items

DATA_DIR = "/Users/tkolar/mel/test_photos/"

def main():

    bookinfo = {}
    items = rmd_get_items()

    file_contents = open(DATA_DIR + "barcodes.txt").read()
    barcodes = file_contents.split("\n")
    barcodes = barcodes[0:-1]   # chop off the (blank) last entry

    image_names = os.listdir(DATA_DIR + "images")
    image_names.sort()

    barcode_index = 0
    for name in image_names:
        print()
        print()
        num_potentials = min(10, len(barcodes) - barcode_index)
        potential_barcodes = barcodes[barcode_index:barcode_index + num_potentials]
        for i,pb in enumerate(potential_barcodes):
            barcode = pb.lstrip("0")
            if barcode not in items:
                continue
            print(i, items[barcode]["Title"])

        img = cv2.imread(DATA_DIR + "images/" + name, 0)
        rotated_img = cv2.rotate(img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
        cv2.imshow(name,img)
        cv2.imshow(name+"R",rotated_img)

        chosen_index = -1
        while(True):
            c = cv2.waitKey(0)

            if c == 13:
                print("default")
                chosen_index = 0
                break
            elif c == ord('q'):
                sys.exit(0)
            elif (chr(c) >= '0') and (chr(c) <= '9'):
                chosen_index = int(chr(c))
                print(chosen_index)
                break
            else:
                print("Invalid input")

        cv2.destroyAllWindows()

        barcode_index += 1
        

    sys.exit(0)    

    for i in range(0, len(image_names)):
        b = barcodes[i].lstrip("0")
        if b not in items:
            continue
        bookinfo[b] = {}
        bookinfo[b]["Image"] = image_names[i]
        bookinfo[b]["ISBN"] = items[b]["ISBN"]
        bookinfo[b]["Title"] = items[b]["Title"]
        bookinfo[b]["Barcode"] = b
        print(bookinfo[b])


    sys.exit(0)
    for barcode,item in items.items():
        checked_out = int(item["# times Checked Out"])
        if checked_out not in checkouts:
            checkouts[checked_out] = 0
        checkouts[checked_out] += 1

    tmp = sorted(checkouts.keys())
    largest_key = tmp[-1]

    totals = []
    counts = []
    foo = []
    for i in range(1, largest_key + 1):
        if i in checkouts:
            totals.append(checkouts[i])
            counts.append(i)
            foo.append("%s" % i)

    p = figure(x_range=foo, plot_height=500, plot_width=1000,
           title="Number of checkouts",
           toolbar_location=None, tools="", x_axis_label="Books",
           y_axis_label="Times Checked Out")

    p.vbar(x=counts, top=totals, width=2)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    show(p)


main()


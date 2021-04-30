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

items = rmd_get_items()

def main():


    outfile = open("/tmp/outfile.txt", "a")
    file_contents = open("/tmp/unmatched_images").read()
    image_names = file_contents.split("\n")
    image_names = image_names[0:-1]   # chop off the (blank) last entry

    index = 0
    for image_name in image_names:
        print("Index: %d", index)
        img = cv2.imread(DATA_DIR + SECTION + "-trimmed" + "/" + image_name, 0)
        rotated_img = cv2.rotate(img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)

        cv2.imshow("Vertical",img)
        cv2.imshow("Horizontal",rotated_img)

        chosen_index = -1
        barbuf = []
        while(True):
            c = cv2.waitKey(0)
            if c == ord('1'):
                sys.exit(0)
            if c == ord('5'):
                barbuf = []
                print("Cleared")
                continue
            if c == 13:
                break;
            if c == 3:
                break;

            barbuf.append(chr(c))

            print(barbuf)

        barbuf_str = "".join(barbuf)
        print(barbuf_str)

        outstr = "%s  :  %s\n" % (image_name, barbuf_str)
        outfile.write(outstr)
        print(outstr)

        print ("\n" * 1)
        
main()


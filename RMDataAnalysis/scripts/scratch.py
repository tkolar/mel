import sys
import os
import csv
import datetime
import json

import pprint
from rmd_common import rmd_get_items
from rmd_common import rmd_get_isbns



items = rmd_get_items()
isbns = rmd_get_isbns()

DATA_DIR = "/Users/tkolar/mel/spines/"

def main():

    pp = pprint.PrettyPrinter(indent=4)

    file = open(DATA_DIR + "conn-F.json")
    connections = json.load(file)

    format = None
    pages = None
    dim = None

    for barcode in connections:
        if barcode == "cursor":
            continue
        if barcode not in items:
            continue
        isbn_number = items[barcode]["ISBN"]
        if isbn_number == "":
            continue
        isbn = isbns[isbn_number]
        if "physical_format" in isbn:
            format = isbn["physical_format"]
        if "number_of_pages" in isbn:
            pages = isbn["number_of_pages"]
        if "physical_dimensions" in isbn:
            dim = isbn["physical_dimensions"]

        print("    ", format, "|||",  pages, "|||", dim)

        if dim == None:
            continue
        dim_split = dim.split()
        if len(dim_split) != 6:
            continue

        sheight, _, swidth, _, sthick, units = dim_split
        if units == "inches":
            height = float(sheight)
            width = float(swidth)
            thick = float(sthick)
        elif units == "centimeters":
            #
            # Replace the , with a . and convert centimeters 
            # to inches
            #
            height = float(sheight.replace(",","."))/2.54
            width = float(swidth.replace(",","."))/2.54
            thick = float(sthick.replace(",","."))/2.54
        else:
            print("Unknown unit:", units)


main()

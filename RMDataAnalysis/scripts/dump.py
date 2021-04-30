import sys
import csv
import datetime
from bokeh.plotting import figure, show
import numpy as np

from rmd_common import rmd_get_items

def main():

    items = rmd_get_items()
    barcodes = []
    file = open("/tmp/k")
    for line in file:
        barcodes.append(line.lstrip("0")[:-1])

    for b in barcodes:
        if b in items:
            i = items[b]
            print(i["Author"])
        else:
            print(b)

main()


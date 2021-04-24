import sys
import csv
import datetime
import numpy as np

from rmd_common import rmd_get_items

def main():

    items = rmd_get_items()
    for i, item in items.items():
        print(item["ISBN"])


main()

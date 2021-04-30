import sys
import csv
import datetime
from bokeh.plotting import figure, show
import numpy as np

from rmd_common import rmd_get_items
from rmd_common import rmd_get_circulation

def main():

    march_first = datetime.date(2021, 3, 1)

    items = rmd_get_items()
    circulation = rmd_get_circulation()

    checkouts = {}

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


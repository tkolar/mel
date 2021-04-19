import sys
import csv
import datetime
from bokeh.plotting import figure, show
import numpy as np

sys.path.append("/Users/tkolar/mel_inventory/data_analysis/RMDataAnalysis")

from rmd_common import rmd_get_items
from rmd_common import rmd_get_circulation

def main():

    weeks = {}
    items = rmd_get_items()
    circulation = rmd_get_circulation()

    one_day = datetime.timedelta(days=1)
    last_day = datetime.datetime(year=2021, month=3, day=1)
    first_day = datetime.datetime(year=2016, month=1, day=3)

    outstanding = {}
    # stock up the outstanding array
    day = first_day
    while day < last_day:
        outstanding[day] = 0
        day += one_day

    # first day
    day = first_day
    while day < last_day:
        if day not in circulation:
            day += one_day
            continue
        day_circ = circulation[day]
        for key,transaction in day_circ.items():
            if transaction["Check In"] == "":
                # It's still checked out, so ignore it
                continue
            #
            #  Walk through the checkout period incrementing
            #  the outstanding count per day
            #
            datestring = transaction["Check Out"]
            mstr, dstr, ystr = datestring.split('/')
            co = datetime.datetime(year=int(ystr), month=int(mstr), day=int(dstr))
            datestring = transaction["Check In"]
            mstr, dstr, ystr = datestring.split('/')
            ci = datetime.datetime(year=int(ystr), month=int(mstr), day=int(dstr))
            d = co   # start at the checkout date
            while d <= ci:
                if d not in outstanding:
                    break;
                outstanding[d] += 1
                d += one_day

        day += one_day

    x = []
    y = []
    day = first_day
    while day < last_day:
        x.append(day)
        y.append(outstanding[day])
        day += one_day

    p = figure(title="Items With Patrons", 
                x_axis_label="Date", x_axis_type='datetime',
                y_axis_label='y',
                width=1000,
                tools="reset")

    p.line(x, y, legend_label="Items", line_width=2, color="blue")

    show(p)

main()


import sys
import csv
import datetime
from bokeh.plotting import figure, show
import numpy as np

sys.path.append("/Users/tkolar/mel_inventory/data_analysis/RMDataAnalysis")

from rmd_common import rmd_get_items
from rmd_common import rmd_get_circulation

def main():

    march_first = datetime.date(2021, 3, 1)

    items = rmd_get_items()
    circulation = rmd_get_circulation()

    for day in circulation:
        circs = circulation[day]
        for entry in circs:
            #
            # If it's recent, skip it.
            #
            mstr, dstr, ystr = circs[entry]["Expected Back"].split("/")
            day = datetime.date(month=int(mstr), day=int(dstr), year=int(ystr))
            if day > march_first:
                continue

            if circs[entry]["Check In"] == "":
                print(circs[entry])

    sys.exit()
    p = figure(title="Checkouts per day", 
                x_axis_label="Date", x_axis_type='datetime',
                y_axis_label='y',
                width=1000,
                tools="reset")


    dates = sorted(circulation.keys())
    x = []
    y = []
    for key in dates:
        x.append(key)
        y.append(len(circulation[key]))

    smooth_y = np.convolve(y, np.ones(30)/30, mode='valid')

    p.line(x, smooth_y, legend_label="Days", line_width=2)

    show(p)


main()


import sys
import csv
from datetime import datetime
from bokeh.plotting import figure, show
import numpy as np

sys.path.append("/Users/tkolar/mel_inventory/inventory_2021/ResourceMateData/")

from rmd_common import rmd_get_items
from rmd_common import rmd_get_circulation

def main():

    items = rmd_get_items()
    circulation = rmd_get_circulation()

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


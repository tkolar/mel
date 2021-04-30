import sys
import csv
import datetime
from bokeh.plotting import figure, show
import numpy as np

from rmd_common import rmd_get_items
from rmd_common import rmd_get_circulation

def main():

    weeks = {}
    items = rmd_get_items()
    circulation = rmd_get_circulation()

    first_day = datetime.datetime(year=2016, month=1, day=3)
    one_week = datetime.timedelta(days=7)
    one_day = datetime.timedelta(days=1)

    # from January 3, 2016 through March 1, 2021
    for i in range(0,270):
        sunday = first_day + one_week * i
        weeks[sunday] = {}
        weeks[sunday]["titles"] = set()
        weeks[sunday]["patrons"] = set()
        for d in range(0,7):
            day_key = sunday + d * one_day
            if day_key not in circulation:
                continue
            day_circ = circulation[day_key]
            for transaction in day_circ:
                t = day_circ[transaction]
                weeks[sunday]["titles"].add(t["Title Info"])
                weeks[sunday]["patrons"].add(t["Patron"])

    week_list = sorted(weeks.keys())
    #for w in week_list:
    #    print(w, len(weeks[w]["titles"]), len(weeks[w]["patrons"]))
        
    p = figure(title="Checkouts and users per week", 
                x_axis_label="Date", x_axis_type='datetime',
                y_axis_label='y',
                width=1000,
                tools="reset")

    x = []
    y1 = []
    y2 = []
    for w in week_list:
        x.append(w)
        y1.append(len(weeks[w]["titles"]))
        y2.append(len(weeks[w]["patrons"]))

    p.line(x, y1, legend_label="Items", line_width=2, color="blue")
    p.line(x, y2, legend_label="Patrons", line_width=2, color="red")

    show(p)

main()


import sys
import csv
import datetime
from bokeh.plotting import figure, show
import numpy as np

from rmd_common import rmd_get_patrons
from rmd_common import rmd_date_from_rmdate

def main():

    patrons = rmd_get_patrons()
    # Last Name
    # First Name
    # Email
    # Barcode
    # Type of Membership
    # Date Added
    # Date Updated
    # Membership Expiration Date
    # Fine Balance

    current = []
    expired = []
    no_expiry = []

    today = datetime.date.today()
    for barcode,patron in patrons.items():
        expiry_str = patron["Membership Expiration Date"]
        if (expiry_str == ""):
            no_expiry.append(patron)
            current.append(patron)
            continue
        expiry = rmd_date_from_rmdate(expiry_str)
        if (expiry < today):
            expired.append(patron)
        else:
            current.append(patron)

    print("current members: ", len(current))
    print("expired members: ", len(expired))
    print("no expiry members: ", len(no_expiry))

    short_timers = 0

    for m in expired:
        expiry_str = m["Membership Expiration Date"]
        expiry = rmd_date_from_rmdate(expiry_str)
        added_str = m["Date Added"]
        added = rmd_date_from_rmdate(added_str)

        membership_length = (expiry - added).days
        if membership_length < 400:
            short_timers += 1

    print("expired memberships <= 1 year long:", short_timers)

    bucket = [0] * 6      # array with six zeroes
    for m in current:
        added_str = m["Date Added"]
        added = rmd_date_from_rmdate(added_str)
        membership_length = (today - added).days
        bucket[int(membership_length / 365)] += 1
    print(bucket)

    labels = ["< 1", "1", "2", "3", "4", "5+"]
    p = figure(x_range=labels, plot_height=500, plot_width=1000,
           title="Number of current members by membership length",
           toolbar_location=None, tools="", x_axis_label = "Years",
           y_axis_label = "Members")

    p.vbar(x=labels, top=bucket, width=1)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    show(p)

main()


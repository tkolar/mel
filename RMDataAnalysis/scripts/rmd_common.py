import sys
import csv
import datetime
import json

ROOTDIR="/Users/tkolar/mel/RMDataAnalysis/" 

#
# items.csv fields
#
# 'Resource Type', 'Title', 'Section', 'Author', 'Publisher', 
# 'Status', '# times Checked Out', 'Accession Date', 'Barcode'
#
def rmd_get_items():
    items = {}
    csvfile = open(ROOTDIR+"items.csv", encoding="latin-1")
    cvsreader = csv.DictReader(csvfile)
    for row in cvsreader:
        barcode = row["Barcode"]
        items[barcode] = row
        truncated_barcode = barcode.lstrip('0')
        items[truncated_barcode] = row

    return(items)

#
# circulation.csv fields
#
# 'Resource Type', 'Title Info', 'Check Out', 'Expected Back', 
# 'Check In', 'Renewals', 'Barcode', 'Patron'
def rmd_get_circulation():
    circulation = {}
    csvfile = open(ROOTDIR+"circulation.csv", encoding="latin-1")
    cvsreader = csv.DictReader(csvfile)
    for row in cvsreader:
        checkout = row["Check Out"]
        barcode = row["Barcode"]
        month, day, year = checkout.split('/')
        day = datetime.datetime(int(year), int(month), int(day))
        if day not in circulation:
            circulation[day] = {}
        circulation[day][barcode] = row

    return(circulation)

#
# patrons.csv fields
#
# Last Name,First Name,Email,Barcode,Type of Membership,
# Date Added,Date Updated,Membership Expiration Date,Fine Balance
#
def rmd_get_patrons():
    items = {}
    csvfile = open(ROOTDIR+"patrons.csv", encoding="latin-1")
    cvsreader = csv.DictReader(csvfile)
    for row in cvsreader:
        barcode = row["Barcode"]
        items[barcode] = row

    return(items)

def rmd_get_isbns():
    file = open(ROOTDIR+"isbns.json")
    isbns = json.load(file)
    return(isbns)



def rmd_date_from_rmdate(rmdate):
    mstr, dstr, ystr = rmdate.split("/")
    day = datetime.date(month=int(mstr), day=int(dstr), year=int(ystr))
    return(day)


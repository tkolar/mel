import sys
import csv
import datetime

ROOTDIR="/Users/tkolar/mel_inventory/data_analysis/RMDataAnalysis/" 

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

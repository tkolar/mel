import sys
import csv


section_map = {
    'Hardcover fict': 'Fiction',
    'Fiction': 'Fiction',
    'Short Stories': 'Fiction',
    'Fantasy': 'Fiction',
    'Horror': 'Fiction',
    'Science Fiction': 'Fiction',

    'Non-fiction': 'Non-fiction',
    '2nd language re': 'Non-fiction',

    'Judd Dolle': 'Judd Dolle',
    'Judd Dolle Span': 'Judd Dolle',
    'Judd Dolle - Re': 'Judd Dolle',

    'Audiobooks': 'Audiobooks',
    'DVD': 'DVD',
    'Puzzles': 'Puzzles',

    '': 'Unknown',
    'Holidays': 'Holidays',

    'Young Adult': 'Young Adult',

    'Children': 'Children',
    'child 900': 'Children',
    'pic. books hard': 'Children',
    'child inter rea': 'Children',
    'child 300': 'Children',
    'pic. books pape': 'Children',
    'child adv. read': 'Children',
    'child 500': 'Children',
    'child 600': 'Children',
    'child mid reade': 'Children',
    'child. Latin Am': 'Children',
    'child early rea': 'Children',
    'Child B.C.': 'Children',
    'large print': 'Children',
    'child 900': 'Children',
    'child anth.': 'Children',
    "Children's DVD": 'Children',
    "Children's Puzz": 'Children',
    'child 800': 'Children',
    'Board Books': 'Children'
    }

#
# items.csv fields
#
# 'Resource Type', 'Title', 'Section', 'Author', 'Publisher', 'Status', '# times Checked Out', 'Accession Date', 'Barcode'
#
def get_book_dict():
    book_dict = {}
    csvfile = open("items.csv", encoding="latin-1")
    cvsreader = csv.DictReader(csvfile)
    for row in cvsreader:
        barcode = row["Barcode"]
        book_dict[barcode] = row

    return(book_dict)


def main():

    book_dict = get_book_dict()
    output = open("missing_by_section.html", "w")

    output.write("""
<html>
<head>
<style>
table, th, td {
}
tr:nth-child(even) {background-color: #DDDDDD;}

table.center {
  margin-left: auto;
  margin-right: auto;
}
</style>
</head>
    """)
    
    shelf_line = 0
    shelf_name = ""
    cubby = ""
    location_names = []
    locations = {}


    output.write("\n<table>\n")
    output.write("\n<caption><h1>Missing items by section</h1></caption>\n")

    #
    #  Go through all the missing items
    #
    all = {}

    section_list = set()
    
    barfile = open(sys.argv[1])
    for line in barfile:
        sline = line[:-1]
        if sline in book_dict:
            section = book_dict[sline]["Section"]
            section = section_map[section]
            section_list.add(section)
            if section not in all:
                all[section] = []
            all[section].append(sline)

    print(all.keys())
    print(section_list)

    for main_section in section_list:
        output.write("<tr><td><br><h3>" + main_section + "</h3></td></tr>\n")
        for barcode in all[main_section]:
            output.write("<tr>")
            if barcode in book_dict:
                section = book_dict[barcode]["Section"]
                title = book_dict[barcode]["Title"]
                text = "<td>%s</td><td>%s</td><td>%.30s</td>\n" % \
                                            (barcode, section, title)
                output.write(text)
            else:
                print("Missing barcode: %s" % barcode)
            output.write("</tr>\n")

    output.write("</table>\n")

    output.write("</html>\n")

main()


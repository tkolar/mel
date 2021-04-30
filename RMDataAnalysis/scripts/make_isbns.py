import os
import json

def main():
    isbns = {}
    dir_list = os.listdir("isbns")
    for isbn in dir_list:
        file = open("isbns/" + isbn)
        entry = json.load(file)
        isbns[isbn] = entry

    outfile = open("isbns.json", "w")
    json.dump(isbns, outfile)


main()

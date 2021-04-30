
import sys
import json


#
# Read it in
#
file = open("conn-F.json")
d = json.load(file)
file.close()

for barcode in d:
    print(d[barcode])
sys.exit(0)

#
#  Add the extra connections
#
ifile = open("/tmp/i")
for line in ifile:
    line = line[:-1]
    filename, barcode = line.split(" ")
    d[barcode] = filename

#
# dump it out
#
file = open("conn-F.json", "w")
json.dump(d, file)

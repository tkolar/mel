
import os
import sys
import subprocess

def main():
    file_text = open("outfile.txt").read()
    lines = file_text.split("\n")
    lines = lines[:-1]

    for l in lines:
        s = l.split(":")
        title = s[1].lstrip()
        print(s[0], title)
        if (title == ""):
            continue
        cmd = ["/usr/bin/grep", "-i", "-H",  "%s" % title, "../items.csv"]
        cmd_output = subprocess.run(cmd, capture_output=True)
        print(cmd_output.stdout)
        print
        print
    

main()

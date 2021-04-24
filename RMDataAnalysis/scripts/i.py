import requests

def main():
    file_text = open("/tmp/is").read()
    isbns = file_text.split("\n")
    isbns = isbns[:-1]

    for isbn in isbns:
        outfile = open("isbns/" + isbn, "w")
        url = "http://openlibrary.org/isbn/" + isbn + ".json"
        print(url)
        r = requests.get(url)
        if r.status_code != 200:
            outfile.write("{\"status_code\": \"%d\"}" % r.status_code)
        else:
            outfile.write(r.text)


main()

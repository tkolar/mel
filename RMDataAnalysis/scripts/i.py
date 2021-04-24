import requests

def main():
    file_text = open("/tmp/is").read()
    isbns = file_text.split("\n")
    isbns = isbns[:-1]

    isbns = ["0006392393"]
    for isbn in isbns:
        outfile = open("isbns/" + isbn, "w")
        url = "http://openlibrary.org/isbn/" + isbn + ".json"
        r = requests.get(url)
        print(r)
        outfile.write(r.text)


main()

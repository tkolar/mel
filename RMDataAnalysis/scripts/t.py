from olclient.openlibrary import OpenLibrary
import olclient.common as common
ol = OpenLibrary()
book = common.Book(isbn=u"9780345426802")
print(book)


import json

import hw8.connect
from hw8.models import Quote, Author
# import connect
# from models import Quote, Author


def autors_add(authors):
    for i in authors:
        i = Author(**i).save()
        print(i)

def quotes_add(qoutes):
    for i in qoutes:
        print(i["author"])
        # get author id to quote
        i["author"] = Author.objects.get(fullname = i["author"]).id
        m = Quote(**i).save()
        # print(m)


if __name__ == '__main__':
    
    with open("authors.json") as file:
        authors = json.load(file)
    autors_add(authors=authors)

    with open("quotes.json") as file:
        qoutes = json.load(file)
    quotes_add(qoutes)
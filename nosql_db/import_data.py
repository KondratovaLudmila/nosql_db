import json
from datetime import datetime

from connect_mongo import connect_to_db
from models import Author, Quote

connect_to_db()

def import_data():
    try:
        with open("authors.json", "r", encoding="utf-8") as jf:
            authors = json.load(jf)
        with open("quotes.json", "r", encoding="utf-8") as jf:
            quotes = json.load(jf)
            
    except Exception as error:
        print(error)
        return
    
    for author in authors:
        if "born_date" in author:
            author["born_date"] = datetime.strptime(author["born_date"], "%B %d, %Y")
        new_author = Author(**author)
        new_author.save()
    
    for quote in quotes:
        if "author" in quote:
            quote["author"] = Author.objects(fullname=quote["author"]).first()
        quote["quote"] = quote["quote"].encode()
        new_quote = Quote(**quote)
        new_quote.save()
    
    
if __name__ == "__main__":
    import_data()


    
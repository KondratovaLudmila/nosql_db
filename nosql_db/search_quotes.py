from mongoengine import QuerySet
import re
import redis
from redis_lru import RedisLRU


from models import Author, Quote
from connect_mongo import connect_to_db

connect_to_db()

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


def convert_to_str(quotes: QuerySet):
    result = ""
    for quote in quotes:
        result += f"author: {quote.author.fullname}\nquote: {quote.quote}\ntags: {', '.join(quote.tags)}\n"

    return result


@cache
def find_by_author(author_name: str):
    author = Author.objects(fullname__regex="^" + author_name)
    quotes = Quote.objects(author__in=author)

    return quotes


@cache
def find_by_tags(tags: tuple):
    regex_tags = []
    for tag in tags:
        regex_tags.append(re.compile("^" + tag))
    quotes = Quote.objects(tags__in=tuple(regex_tags))
    
    return quotes


def parse(line: str) -> tuple:
    result = ()
    type, value = line.split(": ", maxsplit=1)
    
    if type == "name":
        result = (find_by_author, value)
    elif type == "tag":
        result = (find_by_tags, (value,))
    elif type == "tags":
        result = (find_by_tags, value.split(","))
    else:
        raise ValueError("Unrecognised command!")
    
    return result
    

def main():
    user_input = ""
    while True:
        user_input = input("Enter search type (name:/tag:/tags:) value :")
        if user_input == "exit":
            break

        try:
            command, value = parse(user_input)
            result = convert_to_str(command(value))
        except Exception as error:
            result = error

        print(result)

if __name__ == "__main__":
    main()
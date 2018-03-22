"""
This script creates author_name based on author_id for the series collection.
For the comic collection, it maps author_name and series_name.

The author name consists of its first_name, last_name and nickname.
"""

from pymongo import MongoClient

client = MongoClient("mongo")
db = client['bdgest']

def author_by_id(id):
    document = db["authors"].find_one({'author_id': id})
    name = ""
    for x in ["first_name", "last_name", "nickname"]:
        if document.get(x):
            if x == "nickname": name += '"{0}"'.format(document[x])
            else: name += document[x] + " "
    return name.rstrip()

def series_by_id(id):
    document = db["series"].find_one({'series_id': id})
    return document["name"]

for document in db["comics"].find():
    db["comics"].update_one({'url': document['url']}, {'$set': {'author_name': author_by_id(document['author_id'])}}, upsert=False)

for document in db["series"].find():
    db["series"].update_one({'url': document['url']}, {'$set': {'author_name': author_by_id(document['author_id'])}}, upsert=False)

for document in db["comics"].find():
    db["comics"].update_one({'url': document['url']}, {'$set': {'series_name': series_by_id(document['series_id'])}}, upsert=False)

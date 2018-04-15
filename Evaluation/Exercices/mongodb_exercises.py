#sans le text index, la recherche d'un document par les mots qu'il contient ne fonctionne pas

import pandas as pd
from pymongo import MongoClient
import pymongo
import json
from pprint import pprint

df = pd.read_csv("../OUAP-4314/Mongo/data/ks-projects-201801-sample.csv")
df_json = json.loads(df.to_json(orient='records'))

client = MongoClient("localhost", 27017)
db = client['exercise']
db["kickstarter"].remove()
db["kickstarter"].insert(df_json)

#Récupérer les 5 projets ayant reçu le plus de promesse de dons.
db["kickstarter"].find().sort('usd_pledged_real', -1).limit(5)
for x in db["kickstarter"].find().sort('usd_pledged_real', -1).limit(5):
    pprint(x)

#Compter le nombre de projets pour chaque catégorie.
cursor = db.kickstarter.aggregate([{"$group" : {"_id" : "$category", "count" : {"$sum" : 1}}}])
for x in cursor:
    print(x["_id"], x["count"])

#Compter le nombre de projets français ayant été instanciés avant 2016.

for x in db["kickstarter"].find({"country": "FR", "launched":{"$lt": "2016-01-01"}}):
    print(x["launched"])

#Récupérer les projets américains ayant demandé plus de 200 000 dollars.
cursor = db.kickstarter.find({"$and":[{"goal":{"$gte":200000}}, {"country":"US"}]})

#Compter le nombre de projet ayant "Sport" dans leur nom
cursor = db.kickstarter.find({'name': {'$regex': "\\b" + "Sport", '$options': 'i'}})
print(cursor.count())









import pandas as pd
from pymongo import MongoClient
import pymongo

df = pd.read_csv("../OUAP-4314/Mongo/data/USvideos.csv")
df_json = json.loads(df.to_json(orient='records'))

client = MongoClient("localhost", 27017)
db = client['exercise']
db["youtube"].remove()
db["youtube"].insert(df_json)

dict_category = {}
for category in d["items"]:
    dict_category[int(category["id"])] = category["snippet"]["title"]

for document in db["youtube"].find():
    db["youtube"].update({"video_id": document["video_id"]},
                         {"$set": {"category": dict_category[document["category_id"]]}})

#Récupérer toutes les vidéos de la chaîne Apple
for document in db["youtube"].find({"channel_title": "Apple"}):
    print(document)

#Compter le nombre de catégories différentes
print(len(db["youtube"].distinct("category")))

pipeline = [
    {"$group": {"_id":"$category", "count":{"$sum":1}}}
]
for x in db.command('aggregate', 'youtube', pipeline=pipeline, explain=False)["cursor"]["firstBatch"]:
    print(x["_id"], ":", x["count"])

#Si vous ne l'avez pas déjà fait, découper les tags en listes et mettre à jour les tags de chacun des documents avec une requête update.
for document in db["youtube"].find():
    db["youtube"].update_one({"_id": document["_id"]}, 
                         {"$set": {"tags": [tag for tag in document["tags"].split("|")]}})

#Récupérer les vidéos les plus vues.
for document in db["youtube"].find().sort("views", -1).limit(10):
    print(document)

#Compter le nombre moyen de vues en fonction de la catégorie.
pipeline = [
    {"$group": {"_id":"$category", "average_views":{"$avg": "$views"}}}
]
for x in db.command('aggregate', 'youtube', pipeline=pipeline, explain=False)["cursor"]["firstBatch"]:
    print(x["_id"], ":", x["average_views"])

#Récupérer les chaines Youtube avec la plus grande moyenne de likes.
pipeline = [
    {"$group": {"_id":"$channel_title", "average_likes":{"$avg": "$likes"}}},
    {"$sort": {"average_likes": -1}}
]
for x in db.command('aggregate', 'youtube', pipeline=pipeline, explain=False)["cursor"]["firstBatch"]:
    print(x["_id"], ":", x["average_likes"])

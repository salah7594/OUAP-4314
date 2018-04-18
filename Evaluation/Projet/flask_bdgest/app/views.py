"""
page author: first name, last name, nickname, url, country, birth date, death date, image
"""

from flask import render_template, url_for, redirect, request, flash

from .forms import AuthorForm, SeriesForm, ComicForm

from app import app
from datetime import datetime
from pymongo import MongoClient

client = MongoClient("mongo")
db = client['bdgest']

def series_by_id(id):
    document = db["series"].find_one({'_id': id})
    return document["name"]

def author_by_id(id):
    document = db["authors"].find_one({'_id': id})
    name = document["full_name"]
    return name

def table_comic(query):
    list_document = []
    for document in query:
        document_updated = {"redirect_comic": [document["url"], document["title"]]}
        document_updated.update({"redirect_series": ["/series/{0}".format(document["series_id"]), series_by_id(document["series_id"])]})
        document_updated.update({"redirect_author": ["/author/{0}".format(document["author_id"]), author_by_id(document["author_id"])]})
        document_updated.update({key: (document[key] if document.get(key) else "") for key in ("scenario", "illustration", "editor", "legal_deposit")})
        if document_updated.get("legal_deposit"): document_updated.update({"legal_deposit": "{:%m-%Y}".format(document["legal_deposit"])})
        list_document.append(document_updated)

    return list_document

def table_series(query):
    list_document = []
    for document in query:
        document_updated = {"redirect_series": ["/series/{0}".format(document["_id"]), document["name"]]}
        document_updated.update({"redirect_author": ["/author/{0}".format(document["author_id"]), author_by_id(document["author_id"])]})
        document_updated.update({key: (document[key] if document.get(key) else "") for key in ("genre", "origin", "lang")})
        list_document.append(document_updated)

    return list_document

def kardesh(query):
    if query.get("author_name"):
        list_author_id = []
        fetch_name = query["author_name"]

        query_match = {}
        query_match.update({'$or': [{'last_name': {'$regex': "\\b" + fetch_name, '$options': 'i'}},
                                {'first_name': {'$regex': "\\b" + fetch_name, '$options': 'i'}},
                                {'nickname': {'$regex': "\\b" + fetch_name, '$options': 'i'}},
                                ]})
        for document in db["authors"].find(query_match):
            list_author_id.append(document["_id"])
        query.pop("author_name")
        query.update({"author_id": {"$in": list_author_id}})
    
    if query.get("series_name"):
        list_series_id = []
        fetch_name = query["series_name"]

        query_match = {}
        query_match.update({"name": {'$regex': "\\b" + fetch_name.strip(), '$options': 'i'}})
        
        for document in db["series"].find(query_match):
            list_series_id.append(document["_id"])
        query.pop("series_name")
        query.update({"series_id": {"$in": list_series_id}})
    
    return query

@app.route('/', methods=['GET', 'POST'])
def home():

    author_form = AuthorForm()
    series_form = SeriesForm()
    comic_form = ComicForm()

    return render_template('index.html', author_form=author_form, series_form=series_form, comic_form=comic_form)

@app.route('/author', methods=['POST'])
def author():
    output = {}
    author_form = AuthorForm()
    if author_form.validate_on_submit():
        list_document = []

        fetch_name = request.form.get('name', None).strip()
        fetch_country = request.form.get('country', None).strip()

        mongo_formatted_string = {}

        if fetch_name: 
            mongo_formatted_string.update({'$or': [{'last_name': {'$regex': "\\b" + fetch_name, '$options': 'i'}},
                                        {'first_name': {'$regex': "\\b" + fetch_name, '$options': 'i'}},
                                        {'nickname': {'$regex': "\\b" + fetch_name, '$options': 'i'}},
                                        ]})
        if fetch_country:
            mongo_formatted_string.update({'country': {'$regex': "\\b" + fetch_country, '$options': 'i'}})

        if mongo_formatted_string:
            for document in db["authors"].find(mongo_formatted_string):
                document_updated = {"redirect_author": ["/author/{0}".format(document["_id"]), "Go."]}
                document_updated.update({key: (document[key] if document.get(key) else "") for key in ("first_name", "last_name", "nickname", "birth_date", "death_date")})
                if document_updated.get("death_date"): document_updated.update({"death_date": "{:%d-%m-%Y}".format(document["death_date"])})
                if document_updated.get("birth_date"): document_updated.update({"birth_date": "{:%d-%m-%Y}".format(document["birth_date"])})
                list_document.append(document_updated)
            output["list_document"] = list_document

    return render_template('author.html', output=output)


@app.route('/series', methods=['POST'])
def series():
    output = {}
    series_form = SeriesForm()
    if series_form.validate_on_submit():
        dict_fetch = {}
        for x in ['name', 'genre', 'author_name', 'lang', 'origin', 'status']:
            dict_fetch[x] = request.form.get(x, None)

        mongo_formatted_string = {}
    
        for key, value in dict_fetch.items():
            if value:
                if key == 'status': mongo_formatted_string.update({key: int(value)})
                elif key == "author_name": mongo_formatted_string.update({key: value})
                else: mongo_formatted_string.update({key: {'$regex': "\\b" + value.strip(), '$options': 'i'}})
        
        if mongo_formatted_string:
            mongo_formatted_string = kardesh(mongo_formatted_string)
            output["list_document"] = table_series(db["series"].find(mongo_formatted_string))

    return render_template('series.html', output=output)

@app.route('/comic', methods=['POST'])
def comic():
    output = {}
    comic_form = ComicForm()
    if comic_form.validate_on_submit():
        dict_fetch = {}
        for x in ["title", "editor", "collection", "format", "isbn", "author_name", "series_name"]:
            dict_fetch[x] = request.form.get(x, None)

        mongo_formatted_string = {}

        for key, value in dict_fetch.items():
            if value:
                if key == "isbn": mongo_formatted_string.update({key: {'$regex': value, '$options': 'i'}})
                elif key == "author_name": mongo_formatted_string.update({key: value})
                elif key == "series_name": mongo_formatted_string.update({key: value})
                else: mongo_formatted_string.update({key: {'$regex': "\\b" + value.strip(), '$options': 'i'}})

        if mongo_formatted_string:
            mongo_formatted_string = kardesh(mongo_formatted_string)
            output["list_document"] = table_comic(db["comics"].find(mongo_formatted_string))

    return render_template('comic.html', output=output)

@app.route('/author/<author_id>')
def author_id(author_id):
    output = {}
    output["document"] = db["authors"].find_one({"_id": author_id})
    output["list_comic"] = table_comic(db["comics"].find({"author_id": author_id}))
    output["list_series"] = table_series(db["series"].find({"author_id": author_id}))

    pipeline = [
        {"$match": {"author_id": author_id}},
        {"$group": {"_id":"$genre", "count":{"$sum":1}}}
    ]
    output["pie"] = db.command('aggregate', 'series', pipeline=pipeline, explain=False)

    return render_template('author_id.html', output=output)

@app.route('/series/<series_id>')
def series_id(series_id):
    output = {}
    output["document"] = db["series"].find_one({"_id": series_id})
    output["document"].update({"author_name": author_by_id(output["document"]["author_id"])})
    output["list_comic"] = table_comic(db["comics"].find({"series_id": series_id}))

    return render_template('series_id.html', output=output)

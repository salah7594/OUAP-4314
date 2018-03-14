"""
page author: first name, last name, nickname, url, country, birth date, death date, image
"""

from flask import render_template, url_for, redirect, request, flash

from .forms import AuthorForm, SeriesForm, ComicForm

from app import app

from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client['bdgest']

def series_by_id(id):
    document = db["series"].find_one({'series_id': id})
    return document["name"]

def author_by_id(id):
    document = db["authors"].find_one({'author_id': id})
    name = ""
    for x in ["first_name", "last_name", "nickname"]:
        if document.get(x):
            if x == "nickname": name += '"{0}"'.format(document[x])
            else: name += document[x] + " "
    return name.rstrip()

@app.route('/home', methods=['GET', 'POST'])
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
                list_document.append(document)

            output["list_document"] = list_document

    return render_template('author.html', output=output)

@app.route('/series', methods=['POST'])
def series():
    output = {}
    series_form = SeriesForm()
    if series_form.validate_on_submit():
        list_document = []  
        dict_fetch = {}
        for x in ['name', 'genre', 'author_name', 'lang', 'origin', 'status']:
            dict_fetch[x] = request.form.get(x, None)

        mongo_formatted_string = {}
    
        for key, value in dict_fetch.items():
            if dict_fetch.get(key):
                if key == 'status': mongo_formatted_string.update({key: int(value)})
                else: mongo_formatted_string.update({key: {'$regex': "\\b" + value.strip(), '$options': 'i'}})

        if mongo_formatted_string:
            for document in db["series"].find(mongo_formatted_string):
                list_document.append(document)

            output["list_document"] = list_document

    return render_template('series.html', output=output)

@app.route('/comic', methods=['POST'])
def comic():
    output = {}
    comic_form = ComicForm()
    if comic_form.validate_on_submit():
        list_document = []
        dict_author = {}
        dict_fetch = {}

        for x in ["title", "editor", "collection", "format", "isbn"]:
            dict_fetch[x] = request.form.get(x, None)

        mongo_formatted_string = {}

        for key, value in dict_fetch.items():
            if dict_fetch.get(key):
                if key == "isbn": mongo_formatted_string.update({key: {'$regex': value, '$options': 'i'}})
                else: mongo_formatted_string.update({key: {'$regex': "\\b" + value.strip(), '$options': 'i'}})

        if mongo_formatted_string:

            for document in db["comics"].find(mongo_formatted_string):
                list_document.append(document)
                dict_author[document["author_id"]] = author_by_id(document["author_id"])

            output["list_document"] = list_document
            # output["dict_author"] = dict_author

    return render_template('comic.html', output=output)

@app.route('/author/<author_id>')
def author_id(author_id):
    output = {}
    output["document"] = db["authors"].find_one({"author_id": author_id})
    output["list_comic"] = db["comics"].find({"author_id": author_id})
    output["list_series"] = db["series"].find({"author_id": author_id})

    return render_template('author_id.html', output=output)

@app.route('/series/<series_id>')
def series_id(series_id):
    output = {}
    output["document"] = db["series"].find_one({"series_id": series_id})
    output["list_comic"] = db["comics"].find({"series_id": series_id})

    return render_template('series_id.html', output=output)

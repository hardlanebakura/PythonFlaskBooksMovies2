from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from books import *
from movies import *

import routing.booksroutes

app = Flask(__name__)

app.config["SECRET_KEY"] = "secretkey"

all_books = [i.__dict__ for i in all_books]

app.add_url_rule('/', view_func=routing.booksroutes.index)

@app.route("/api")
def api():
    return jsonify("all", all_books)

@app.route("/api/books/<string:category>")
def apicategory(category):
    books = booksForOneGenre(category)
    return jsonify("{}".format(category), books)

@app.route("/api/movies/<string:genre>")
def apigenre(genre):
    movies = getTopMoviesByGenre(genre)
    return jsonify("{}".format(genre), movies)

if (__name__ == "__main__"):
    app.run(debug=True)

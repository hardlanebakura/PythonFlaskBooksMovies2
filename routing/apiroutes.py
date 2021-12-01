from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from books import *
from movies import *

def api():
    return jsonify("all", all_books)

def apicategory(category):
    books = booksForOneGenre(category)
    return jsonify("{}".format(category), books)

def apigenre(genre):
    movies = getTopMoviesByGenre(genre)
    return jsonify("{}".format(genre), movies)
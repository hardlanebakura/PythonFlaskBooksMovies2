from flask import Flask, render_template, request, redirect, url_for, jsonify, session

import routing.booksroutes
import routing.moviesroutes
import routing.apiroutes

app = Flask(__name__)

app.config["SECRET_KEY"] = "secretkey"

app.add_url_rule('/', view_func=routing.booksroutes.index)
app.add_url_rule('/topbooks', view_func=routing.booksroutes.topbooks)
app.add_url_rule('/topbooks/<int:id>', view_func=routing.booksroutes.topbook)
app.add_url_rule('/books/<int:id>', view_func=routing.booksroutes.book)
app.add_url_rule('/author/<string:author>', view_func=routing.booksroutes.author)
app.add_url_rule('/books/<string:author><int:id>', view_func=routing.booksroutes.bookbyauthor)
app.add_url_rule('/categories', view_func=routing.booksroutes.categories, methods=["GET", "POST"])
app.add_url_rule('/categories/<int:categoryid>', view_func=routing.booksroutes.category)
app.add_url_rule('/popularauthors', view_func=routing.booksroutes.popularwriters)
app.add_url_rule('/books/wordcloud', view_func=routing.booksroutes.bookswordcloud)

app.add_url_rule('/movies', view_func=routing.moviesroutes.movies)
app.add_url_rule('/movie/<int:movieid>', view_func=routing.moviesroutes.movie)
app.add_url_rule('/topmovies', view_func=routing.moviesroutes.topmovies)
app.add_url_rule('/topmovies/<int:movieid>', view_func=routing.moviesroutes.topmovie)
app.add_url_rule('/genres', view_func=routing.moviesroutes.genres, methods=["GET", "POST"])
app.add_url_rule('/genres/<int:genreid>', view_func=routing.moviesroutes.genre)
app.add_url_rule('/movies/wordcloud', view_func=routing.moviesroutes.movieswordcloud)
app.add_url_rule('/movies/stats', view_func=routing.moviesroutes.moviestats)

app.add_url_rule('/api', view_func=routing.apiroutes.api)
app.add_url_rule('/api/books/<string:category>', view_func=routing.apiroutes.apicategory)
app.add_url_rule('/api/movies/<string:genre>', view_func=routing.apiroutes.apigenre)

if (__name__ == "__main__"):
    app.run(debug=True)

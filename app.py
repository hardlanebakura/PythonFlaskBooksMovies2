from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from books import *
from movies import *

app = Flask(__name__)

app.config["SECRET_KEY"] = "secretkey"

@app.route("/")
def index():
    session["category"] = randomcategory_u
    books = booksForOneGenre(randomcategory_u)
    return render_template("index.html", books = books, randomcategory = randomcategory_u)

@app.route("/topbooks")
def topbooks():
    print(rankonebestsellers)
    return render_template("topbooks.html", books = rankonebestsellers)

@app.route("/topbooks/<int:id>")
def topbook(id):
    book = rankonebestsellers[id - 1]
    return render_template("topbook.html", book = book, randomcategory = book["list_name"])

@app.route("/books/<int:id>")
def book(id):
    return render_template("book.html", book=booksForOneGenre(session["category"])[id - 1],
                           randomcategory=session["category"])

@app.route("/author/<string:author>")
def author(author):
    for i in range(len(listofauthors_filteredout)):
        if listofauthors_filteredout[i] == author:
            k = i
            break
    books = getBooksByAuthor(listofauthors[k])
    books1 = [getInfoForOneBook(i) for i in books]
    for i in range(len(books1)):
        books1[i]["id"] = i
    return render_template("author.html", books = books1, author = author)

@app.route("/books/<string:author>/<int:id>")
def bookbyauthor(author, id):
    for i in range(len(listofauthors_filteredout)):
        if listofauthors_filteredout[i] == author:
            k = i
            break
    books = getBooksByAuthor(listofauthors[k])
    books1 = [getInfoForOneBook(i) for i in books]
    for i in range(len(books1)):
        books1[i]["id"] = i
    return render_template("booksbyauthor.html", book = books1[id])

@app.route("/categories", methods = ["GET", "POST"])
def categories():
    if (request.method == "POST"):
        category = request.form.get("categories")
        session["category"] = category
        #print(request.form.get("categories"))
        for i in range(len(genres_u)):
            if (genres_u[i]) == category:
                k = i
                break
        return redirect("/categories/{}".format(k))
    else:
        session["category"] = randomcategory_u
        books = booksForOneGenre(randomcategory_u)
        return render_template("categories.html", all_books = all_books, books = books, books_genres = genres_u, randomcategory = randomcategory_u)

@app.route("/categories/<int:categoryid>")
def category(categoryid):
    chosencategory = session["category"]
    books = booksForOneGenre(chosencategory)
    print(chosencategory)
    return render_template("category.html",  all_books = all_books, books = books, books_genres = genres_u, randomcategory = genres_u[categoryid])

@app.route("/category/books/<int:id>")
def bookincategory(id):
    return render_template("book.html", book=booksForOneGenre(session["category"])[id - 1],
                           randomcategory=session["category"])

@app.route("/popularauthors")
def popularwriters():
    return render_template("popularauthors.html", popularauthors = popularauthors)

@app.route("/bookswordcloud")
def bookswordcloud():
    return render_template("bookswordcloud.html")

@app.route("/movies")
def movies():
    session["genre"] = randomgenre
    moviesinrandomgenre = getTopMoviesByGenre(randomgenre)[:40]
    return render_template("movies.html", movies = moviesinrandomgenre, randomgenre = randomgenre)

@app.route("/genres", methods = ["GET", "POST"])
def genres():
        if (request.method == "POST"):
            category = request.form.get("categories")
            session["genre"] = category
            for i in range(len(listofallgenres)):
                if (listofallgenres[i]) == category:
                    k = i
                    break
            return redirect("/genres/{}".format(k))
        else:
            movies_genres = getAllGenres()
            session["category"] = randomcategory_u
            books = booksForOneGenre(randomcategory_u)
            movies = getTopMoviesByGenre(randomgenre)
            return render_template("genres.html", all_books=all_books, movies = movies, books_genres=genres_u, movies_genres = movies_genres,
                                   randomgenre = randomgenre)

@app.route("/genres/<int:genreid>")
def genre(genreid):
    chosencategory = session["genre"]
    books = booksForOneGenre(chosencategory)
    movies = getTopMoviesByGenre(chosencategory)
    return render_template("genre.html", all_movies = listoftopmovies, movies = movies, movies_genres = listofallgenres,
                           randomgenre = chosencategory)

@app.route("/movieswordcloud")
def movieswordcloud():
    return render_template("movieswordcloud.html")

@app.route("/movies/<int:movieid>")
def movie(movieid):
    movies = getTopMoviesByGenre(session["genre"])
    return render_template("movie.html", movie = movies[movieid-1])

@app.route("/movies/stats")
def moviestats():
    return render_template("moviestats.html")

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

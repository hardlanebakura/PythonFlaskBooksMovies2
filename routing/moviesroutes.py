from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from books import *
from movies import *

listoftopmovies = [i.__dict__ for i in listoftopmovies]

def movies():
    session["genre"] = randomgenre
    moviesinrandomgenre = [i.__dict__ for i in getTopMoviesByGenre(randomgenre)[:40]]
    return render_template("movies.html", movies = moviesinrandomgenre, randomgenre = randomgenre)

def topmovies():
    session["genre"] = randomgenre
    moviesinrandomgenre = [i.__dict__ for i in getTopMoviesByGenre(randomgenre)[:40]]
    return render_template("topmovies.html", movies = moviesinrandomgenre, randomgenre = randomgenre)

def topmovie(movieid):
        movies = [i.__dict__ for i in getTopMoviesByGenre(session["genre"])[:40]]
        return render_template("movie.html", movie=movies[movieid - 1])

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
            movies = [i.__dict__ for i in getTopMoviesByGenre(randomgenre)[:40]]
            return render_template("genres.html", movies = movies, movies_genres = movies_genres,
                                   randomgenre = randomgenre)

def genre(genreid):
    chosencategory = session["genre"]
    movies = [i.__dict__ for i in getTopMoviesByGenre(chosencategory)[:40]]
    return render_template("genre.html", all_movies = listoftopmovies, movies = movies, movies_genres = listofallgenres,
                           randomgenre = chosencategory)

def movieswordcloud():
    return render_template("movieswordcloud.html")

def movie(movieid):
    movies = [i.__dict__ for i in getTopMoviesByGenre(session["genre"])[:40]]
    return render_template("movie.html", movie = movies[movieid-1])

def moviestats():
    return render_template("moviestats.html")
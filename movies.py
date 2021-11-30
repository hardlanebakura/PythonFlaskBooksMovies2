import requests
import time
from random import randrange
from collections import Counter
from tmdbv3api import TMDb
from tmdbv3api import Movie
from langcodes import *
from api_keys import api_key_movies
import itertools

from mongocollections import Database

movie = Movie()
tmdb = TMDb()
tmdb.api_key = api_key_movies
responsegenres = requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key={}&language=en-US".format(tmdb.api_key)).json()[
    "genres"]

class Movie:

    newid = itertools.count()

    def __init__(self, item):
        self.new_id = next(Movie.newid)
        self.id = item["id"]
        self.original_language = item["original_language"]
        self.title = item["title"]
        self.overview = item["overview"]
        if "genre_ids" in item:
            self.genres = getMoviesGenres(item["genre_ids"])
        if "genres" in item:
            self.genres = item["genres"]
        self.release_date = item["release_date"][:4]
        self.popularity = item["popularity"]
        self.vote_average = item["vote_average"]
        if "poster_path" in item:
            self.image = item["poster_path"]
        if "image" in item:
            self.image = item["image"]
        if "rank" in item:
            self.rank = item["rank"]
        self.original_title = item["original_title"]

    def __repr__(self):
        r = dict(self.__dict__)
        del r["new_id"]
        return "Movie " + str(self.new_id) + " : " + str(r)

def getAllGenres():

    listofallgenres = [item["name"] for item in responsegenres if item["name"] != "Documentary"]
    return listofallgenres

listofallgenres = getAllGenres()

randomgenre = getAllGenres()[randrange(len(getAllGenres()))]

def getMoviesGenres(genres):

    response = requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key={}&language=en-US".format(tmdb.api_key)).json()["genres"]
    listofgenres = []
    if not isinstance(genres, list):
        raise TypeError("Expected list input")
    for genre in genres:
        if not isinstance(genre, int):
            raise TypeError("Expected int input")
        for item in response:
            if item["id"] == genre:
                listofgenres.append(item["name"])
    return listofgenres

def getTopMovies():

    #the maximum pages are 466
    listoftopmovies = []
    for i in range(1,41):
        response = requests.get("https://api.themoviedb.org/3/movie/top_rated?api_key={tmdb}&language=en-US&page={i}".format(tmdb = tmdb.api_key, i = i)).json()["results"]
        for item in response:
            Movie1 = Movie(item)
            listoftopmovies.append(Movie1)
            Database.insertOne("movies3", Movie1.__dict__)
            print("Writing to the database, please wait...")
    return listoftopmovies

#commented out in order to stop multiple adds to the database
#getTopMovies()
listoftopmovies = [Movie(item) for item in Database.findAll("movies3", {})]
listoftoptitles = [item.title for item in listoftopmovies]

def getTopMoviesByGenre(genre):
    movies = []
    if not isinstance(genre, str):
        raise TypeError("Expected string input")
    counter = 1
    for movie in listoftopmovies:
        genres = movie.genres
        if genre in genres:
             movies.append(movie)
             movies[-1].rank = counter
             counter = counter + 1
    #print(movies)
    return movies

getTopMoviesByGenre("Adventure")

getTopMoviesByGenre(randomgenre)

def getTopMoviesByLanguage():
    listofalllanguages = [movie.original_language for movie in listoftopmovies if movie.original_language != "cn"]
    listoftoplanguages = [{k:v} for k, v in Counter(listofalllanguages).most_common()]
    return listoftoplanguages

topmoviesbylanguage = getTopMoviesByLanguage()
acronymstolanguages = []
for item in topmoviesbylanguage:
    for k in item:
        acronymstolanguages.append({k:Language.get(k).display_name()})

def getTopMoviesGenresChart():
    listofallmoviegenres = []
    for movie in listoftopmovies:
        for i in movie.genres:
            listofallmoviegenres.append(i)
    topmoviesbygenres = [{k:v} for k, v in Counter(listofallmoviegenres).most_common()]
    return topmoviesbygenres

topmoviesbygenres = getTopMoviesGenresChart()

#Database.dropCol("movies3")
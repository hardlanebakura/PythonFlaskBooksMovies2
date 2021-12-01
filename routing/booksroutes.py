from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from books import *

all_books = [i.__dict__ for i in all_books]

def index():
    session["category"] = randomcategory_u
    books = [i.__dict__ for i in booksForOneGenre(randomcategory_u)]
    print(books)
    return render_template("index.html", books = books, randomcategory = randomcategory_u)

def topbooks():
    books = [i.__dict__ for i in rankonebestsellers]
    return render_template("topbooks.html", books = books)

def topbook(id):
    book = rankonebestsellers[id - 1]
    return render_template("topbook.html", book = book, randomcategory = book.list_name)

def book(id):
    return render_template("book.html", book=booksForOneGenre(session["category"])[id - 1],
                           randomcategory=session["category"])

def bookauthor(author):
    for i in range(len(listofauthors_filteredout)):
        if listofauthors_filteredout[i] == author:
            k = i
            break
    books = getBooksByAuthor(listofauthors[k])
    books1 = [getInfoForOneBook(i) for i in books]
    for i in range(len(books1)):
        books1[i]["id"] = i
    return render_template("author.html", books = books1, author = author)

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

def categories():
    if (request.method == "POST"):
        category = request.form.get("categories")
        session["category"] = category
        #print(request.form.get("categories"))
        for i in range(len(genres_u)):
            if (genres_u[i]) == category:
                k = i
                break
        return redirect("/books/categories/{}".format(k))
    else:
        session["category"] = randomcategory_u
        books = [i.__dict__ for i in booksForOneGenre(randomcategory_u)]
        return render_template("categories.html", all_books = all_books, books = books, books_genres = genres_u, randomcategory = randomcategory_u)

def category(categoryid):
    chosencategory = session["category"]
    books = [i.__dict__ for i in booksForOneGenre(chosencategory)]
    print(chosencategory)
    return render_template("category.html",  all_books = all_books, books = books, books_genres = genres_u, randomcategory = genres_u[categoryid])

def bookincategory(id):
    return render_template("book.html", book=booksForOneGenre(session["category"])[id - 1],
                           randomcategory=session["category"])

def popularwriters():
    return render_template("popularauthors.html", popularauthors = popularauthors)

def bookswordcloud():
    return render_template("bookswordcloud.html")

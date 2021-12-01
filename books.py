import requests
import time
from random import randrange
from collections import Counter, OrderedDict
from mongocollections import Database
from api_keys import api_key_books
import itertools

response = requests.get("https://api.nytimes.com/svc/books/v3/lists/names.json?api-key={}".format(api_key_books))

#categories of books
genres_u = [i['list_name'] for i in (response.json()['results'])]
genres_l = [i['list_name_encoded'] for i in (response.json()['results'])]
#bestselling books from a random category
random_element = randrange(len(genres_u))
randomcategory_u = genres_u[random_element]
randomcategory_l = genres_l[random_element]

bookcategories = ['rank', 'title', 'author', 'description', 'book_image', 'book_review_link']

class Book:

    newid = itertools.count()
    def __init__(self, item):
        self.new_id = next(Book.newid)
        self.rank = item["rank"]
        self.title = item["title"]
        self.author = item["author"]
        self.description = item["description"]
        self.image = item["image"]
        self.review_link = item["review_link"]
        self.list_name = item["list_name"]
        self.list_name_encoded = item["list_name_encoded"]
        if "top_book_id" in item:
            self.top_book_id = item["top_book_id"]


        if not(isinstance(self.rank, int)):
            raise TypeError("Expected int input")
        if not(isinstance(self.title , str)):
            raise TypeError("Expected string input")
        if not(isinstance(self.author , str)):
            raise TypeError("Expected string input")
        if not(isinstance(self.description , str)):
            raise TypeError("Expected string input")
        if not(isinstance(self.image , str)):
            raise TypeError("Expected string input")
        if not(isinstance(self.review_link , str)):
            raise TypeError("Expected string input")
        if not(isinstance(self.list_name , str)):
            raise TypeError("Expected string input")
        if not(isinstance(self.list_name_encoded , str)):
            raise TypeError("Expected string input")

        #add more unit tests later
        if (self.rank < 1):
            raise ValueError("Rank must be positive number")

    def addTopBookId(self, top_book_id):
        self.top_book_id = top_book_id

    def __repr__(self):
        r = dict(self.__dict__)
        del r["new_id"]
        return "Book " + str(self.new_id) + " : " + str(r)

def toBooks(item):
    return item

def booksForOneGenre(genre):
    books = []
    if not (isinstance(genre, str)):
        raise TypeError("Expected string input")
    #selected_index = genres_u.index(genre)
    list_name = genre
    list_name_encoded = genres_l[genres_u.index(genre)]
    response = requests.get("https://api.nytimes.com/svc/books/v3/lists/current/{}.json?api-key={}".format(list_name_encoded, api_key_books))
    if response.status_code != 200:
        raise TypeError("Expected genre input")
    books_for_chosen_genre = response.json()["results"]["books"]
    for item in books_for_chosen_genre:
        item["list_name"] = list_name
        item["list_name_encoded"] = list_name_encoded
        item["image"] = item["book_image"]
        item["review_link"] = item["book_review_link"]
        Book1 = Book(item)
        books.append(Book1)
    return books

def addAllBooks():

    for i in range(len(genres_u)):
        booksingenre = booksForOneGenre(genres_u[i])

        for j in range(len(booksingenre)):
            book = booksingenre[j]
            Database.insertOne("books1", book.__dict__)
            print("Adding to the database, please wait...")
        if i < 7:
            time.sleep(12)
        else:
            time.sleep(7)
        #it's needed to wait for API calls per minute
        pass

#commented out in order to stop multiple long waits and unnecessary adds to the database
#addAllBooks()

books = booksForOneGenre(randomcategory_u)

all_books = [Book(item) for item in Database.findAll("books1", {})]

listofallbooktitles = []
for i in range(len(all_books)):
    listofallbooktitles.append(all_books[i].title)

# sometimes the same book is listed in different genres, this should be filtered
def findUniqueBooks(books):
    uniquebooks = []
    if not (isinstance(books, list)):
        raise TypeError("Expected list input")
    for i in books:
        if not (isinstance(i, Book)):
            raise TypeError("Expected list of books")
        if i.title not in uniquebooks:

            uniquebooks.append(i.title)
    #uniquebooks = sorted(uniquebooks, key=lambda d: d['author'])
    return uniquebooks

uniquebooks = findUniqueBooks(all_books)
uniquebooks.sort()

def getBooksByAuthor(writer):
    #removes duplicate books that are in multiple categories
    if not (isinstance(writer, str)):
        raise TypeError("Expected string input")
    listofbooksbyauthor = [Book(i) for i in Database.findAll("books1", {"author":writer})]
    books = findUniqueBooks(listofbooksbyauthor)
    return books



listofauthors = []
for item in Database.findAll("books1", {}):
    listofauthors.append(item["author"])

def getPopularAuthors():
    listofpopularauthors = []
    for i in range(len(listofauthors)):
        if len(getBooksByAuthor(listofauthors[i])) > 1:
            listofpopularauthors.append(listofauthors[i])
    #removing the list duplicates
    listofpopularauthors = [i for (i,v) in Counter(listofpopularauthors).items() if v > 1]
    listofpopularauthors.sort()
    return listofpopularauthors

popularauthors = getPopularAuthors()

#need list of author wuth spaces removed to handle routing for one author

def getAllRankOneBestsellers():
    #rankonebestsellers1 = [i for i in col.find({"rank":1}, {"_id":0})]
    rankonebestsellers1 = [Book(item).__dict__ for item in Database.findAll("books1", {"rank": 1})]
    #some bestsellers appear in multipre genres, need to filter them out
    rankonetitles1 = [book["title"] for book in rankonebestsellers1]
    rankonetitles = []
    for title in rankonetitles1:
        if title not in rankonetitles:
            rankonetitles.append(title)
    rankonebestsellers = []
    #this variable is needed in order to render the "TOP BOOKS" page
    counter = 0
    print(rankonetitles)
    #print(rankonebestsellers1)
    for title in rankonetitles:
        Book1 = Book(Database.find("books1", {"rank":1,"title":title}))
        print(Book1)
        j = counter + 1
        Book1.addTopBookId(j)
        #list1[0].id = counter + 1
        counter = counter + 1
        rankonebestsellers.append(Book1)
    print(rankonebestsellers)
    return rankonebestsellers

rankonebestsellers = getAllRankOneBestsellers()

def getInfoForOneBook(booktitle):
    infoforonebook = Database.find("books1", {"title":booktitle})
    return infoforonebook

listofauthors = list(OrderedDict.fromkeys(listofauthors))
listofauthors_filteredout = [i.replace(" ", "") for i in listofauthors]
getAllRankOneBestsellers()

#Database.dropCol("books1")
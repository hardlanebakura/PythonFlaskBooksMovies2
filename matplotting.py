#import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sb
from wordcloud import WordCloud
from collections import Counter
from movies import listoftoptitles, topmoviesbylanguage, acronymstolanguages, topmoviesbygenres
from books import listofallbooktitles

def getWordCloudTitles(listoftitles, genre):

    unique_string=(" ").join(listoftitles)
    wordcloud = WordCloud(width = 1000, height = 500, random_state = 1).generate(unique_string)
    plt.figure(figsize=(15,8))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig("static/images/wordcloudfor{}titles".format(genre) +".png")
    #plt.show()
    plt.close()

    return [unique_string, wordcloud]

wordcloudbooks = getWordCloudTitles(listofallbooktitles, "books")
wordcloudmovies = getWordCloudTitles(listoftoptitles, "movies")
#by default most common words in a sentence are omitted

def wordsInPopularBooks():

    wordsinpopularbooks = [i for i in getWordCloudTitles(listofallbooktitles, "books")[0].split(" ")]
    result = list(dict.fromkeys([item for items, c in Counter(wordsinpopularbooks).most_common()
                                          for item in [items] * c]))[:100]
    return result

wordsInPopularBooks()

def pieChartLanguages():
    labels = []
    sizes = []
    others = {"Others":0}
    for item in topmoviesbylanguage:
        for key in item:
            if item[key] > 3:
                for acronym in acronymstolanguages:
                    for acro in acronym:
                        if key == acro:
                            labels.append(acronym[acro])
        for val in item.values():
            if val > 3:
                sizes.append(val)
            else:
                others["Others"] = others["Others"] + 1
    labels.append("Others")
    sizes.append(others["Others"])
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, shadow=False, startangle=90, labeldistance=1.1, autopct="%d", pctdistance=0.9)
    ax1.axis('equal')
    plt.legend(labels = labels, loc = "center left")
    plt.tight_layout()
    fig1.set_size_inches(8, 6)
    plt.subplots_adjust(left=0.0, bottom=0.1, right=1.05)
    plt.savefig("static/images/chartformovielanguages.png")

pieChartLanguages()

def pieChartGenres():
    labels = []
    sizes = []
    for item in topmoviesbygenres:
        for key in item:
            labels.append(key)
        for val in item.values():
            sizes.append(val)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, shadow=False, startangle=90, labeldistance=1.1, autopct="%d", pctdistance=0.9)
    ax1.axis('equal')
    plt.legend(labels=labels, loc="center left")
    plt.tight_layout()
    fig1.set_size_inches(8, 6)
    plt.subplots_adjust(left=0.0, bottom=0.1, right=1.05)
    plt.savefig("static/images/chartformoviegenres.png")

pieChartGenres()
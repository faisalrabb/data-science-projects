import argparse
import math
import os,sys
import os.path as osp
import json
import pandas as pd
import re
import string


def dialogprocessor(mystring):
    punctuationchars = re.escape(string.punctuation)

    #remove links
    newstring = re.sub(r"https:(\/\/t\.co\/([A-Za-z0-9]|[A-Za-z]){10})", '', mystring)

    #remove punctuation
    newstring = re.sub(r'['+punctuationchars+']', ' ',newstring)

    #remove non alphanumeric
    newstring = re.sub(r'[\W_]+', ' ', newstring)

    wordlist = newstring.split()
    for i in range(len(wordlist)):
        wordlist[i] = wordlist[i].lower()

    #print(wordlist)

    stopwordsfile = open("../data/stopwords.txt", 'r')


    lines = stopwordsfile.readlines()

    for line in lines:
        for badword in line.split():

            while badword in wordlist:
                #print("lit")
                wordlist.remove(badword)

    wordcount = {}
    for word in wordlist:
        if word not in wordcount:
            wordcount[word] = 1
        else:
            wordcount[word] += 1

    #print(wordcount)
    return wordcount

def main():
    df = pd.read_csv("../data/Dune_1000_annotated.csv", header=0)
    #print(df.head())

    df['wordfreq'] = df['text'].apply(lambda x: dialogprocessor(x))

    #frequency of all words in all posts
    allwords = {}
    for index, row in df.iterrows():
        currentrowwords = row['wordfreq']
        for key in currentrowwords:
            if key in allwords:
                allwords[key] += 1

            else:
                allwords[key] = 1

    #idf calculation
    for key in allwords:
        allwords[key] = math.log10(1000 / allwords[key])

    print(allwords)

    #Calculating TF for each topic
    actors = {}
    awards = {}
    book = {}
    cinema = {}
    review = {}
    sound = {}
    theatre = {}
    other = {}

    for index, row in df.iterrows():
        currentrowwords = row['wordfreq']
        currenttopic = row['topic']

        if currenttopic == "actors or characters":
            for key in currentrowwords:
                if key in actors:
                    actors[key] += currentrowwords[key]

                else:
                    actors[key] = currentrowwords[key]

        elif currenttopic == "awards or nomination":
            for key in currentrowwords:
                if key in awards:
                    awards[key] += currentrowwords[key]

                else:
                    awards[key] = currentrowwords[key]



        elif currenttopic == "book":
            for key in currentrowwords:
                if key in book:
                    book[key] += currentrowwords[key]

                else:
                    book[key] = currentrowwords[key]

        elif currenttopic == "cinematography or videography":
            for key in currentrowwords:
                if key in cinema:
                    cinema[key] += currentrowwords[key]

                else:
                    cinema[key] = currentrowwords[key]

        elif currenttopic == "review or commentary":
            for key in currentrowwords:
                if key in review:
                    review[key] += currentrowwords[key]

                else:
                    review[key] = currentrowwords[key]

        elif currenttopic == "soundtrack or sound quality":
            for key in currentrowwords:
                if key in sound:
                    sound[key] += currentrowwords[key]

                else:
                    sound[key] = currentrowwords[key]

        elif currenttopic == "theatre or streaming service":
            for key in currentrowwords:
                if key in theatre:
                    theatre[key] += currentrowwords[key]

                else:
                    theatre[key] = currentrowwords[key]

        else:
            for key in currentrowwords:
                if key in other:
                    other[key] += currentrowwords[key]

                else:
                    other[key] = currentrowwords[key]

    for key in actors:
        actors[key] = actors[key] * allwords[key]

    for key in other:
        other[key] = other[key] * allwords[key]

    for key in awards:
        awards[key] = awards[key] * allwords[key]

    for key in book:
        book[key] = book[key] * allwords[key]

    for key in cinema:
        cinema[key] = cinema[key] * allwords[key]

    for key in sound:
        sound[key] = sound[key] * allwords[key]

    for key in review:
        review[key] = review[key] * allwords[key]

    for key in theatre:
        theatre[key] = theatre[key] * allwords[key]

    actors = sorted(actors.items(), key=lambda item: item[1],reverse= True)[0:10]

    other = sorted(other.items(), key=lambda item: item[1], reverse=True)[0:10]

    cinema = sorted(cinema.items(), key=lambda item: item[1], reverse=True)[0:10]

    sound = sorted(sound.items(), key=lambda item: item[1], reverse=True)[0:10]

    review = sorted(review.items(), key=lambda item: item[1], reverse=True)[0:10]

    theatre = sorted(theatre.items(), key=lambda item: item[1], reverse=True)[0:10]

    awards = sorted(awards.items(), key=lambda item: item[1], reverse=True)[0:10]

    book = sorted(book.items(), key=lambda item: item[1], reverse=True)[0:10]

    results = {
        "review":review,
        "theatre or streaming service": theatre,
        "book": book,
        "actors or characters" : actors,
        "awards or nomination" : awards,
        "cinematography or videography": cinema,
        "soundtrack or sound quality": sound,
        "other": other
    }
    with open("../data/top10tfidf.json", 'w') as output:
        json.dump(results, output,indent= 2)

if __name__ == '__main__':
        main()
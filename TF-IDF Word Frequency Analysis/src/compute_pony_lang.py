import json
import argparse
import os, sys
from math import log
ponies = ["twilight sparkle","applejack","rarity","pinkie pie","rainbow dash","fluttershy"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',required=True, dest='c', help="word count path")
    parser.add_argument('-n', required=True, dest='n', help="num words")
    args=parser.parse_args()
    print(get_stats(args.c, args.n))

def get_stats(fname, n):
    with open(fname, 'r') as c:
        js = json.load(c)
    result={}
    for pony in ponies:
        sorted_words = calc_tf_idf(js, pony)
        words = sorted_words[0:int(n)]
        ranked_words = []
        for l in words:
            ranked_words.append(l[0])
        result[pony] = ranked_words
    return json.dumps(result, indent=4)



def calc_tf_idf(js, pony):
    words = {}
    for word, value in js[pony].items():
        tf_idf = value * idf(word, js)
        words[word] = tf_idf
    #sort 
    return list(sorted(words.items(), key=lambda x: x[1], reverse=True))

def idf(word, js):
    num = 0
    for pony in ponies:
        if word in js[pony].keys():
            num+=1
    return log(len(ponies)/num)
    

if __name__=="__main__":
    main()
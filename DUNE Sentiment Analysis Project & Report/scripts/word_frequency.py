import csv
import argparse
import os, sys
import os.path as osp
import emoji
import re 

path = osp.dirname(__file__)
with open(osp.join(path, "..", "data", "stopwords.txt")) as sw:
    stopwords = sw.read()

def main():
    positive={}
    negative={}
    neutral = {}
    parser = argparse.ArgumentParser()
    parser.add_argument('-i',required=True, dest='i', help="input file NAME as it appears in data folder")
    args=parser.parse_args()
    data_path = osp.join(path, "..", "data", args.i)
    with open(data_path, 'r') as data:
        reader = csv.DictReader(data)
        for row in reader:
            words = re.sub(emoji.get_emoji_regexp(), " ", row["text"])
            words = re.sub(r"[^a-zA-Z0-9]", " ",words)
            words = re.sub(r'http\S+', ' ', words)
            words = words.split(" ")
            if row["sentiment"] == "positive":
                for word in words:
                    add_freq(positive, word)
            elif row["sentiment"] == "neutral":
                for word in words:
                    add_freq(neutral, word)
            elif row["sentiment"] == "negative":
                for word in words:
                    add_freq(negative, word)
    for i in range(3):
        positive_word = max(positive, key=positive.get)
        neutral_word = max(neutral, key=neutral.get)
        negative_word = max(negative, key=negative.get)
        print(f"Positive word #{i+1}: {positive_word}")
        print(f"Negative word #{i+1}: {negative_word}")
        print(f"Neutral word #{i+1}: {neutral_word}")
        positive[positive_word] = 0
        negative[negative_word] = 0
        neutral[neutral_word] = 0
        print("________")
    
    
    

def add_freq(d, word):
    word = word.lower()
    if word == "amp":
        return
    if "dune" in word or word in stopwords:
        return
    if word not in d.keys():
        d[word] = 1
    else:
        d[word] += 1

if __name__=="__main__":
    main()
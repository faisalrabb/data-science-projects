import json
import argparse
import os, sys
import csv
from pathlib import Path

punctuation="()[],-.?!:;#&"
ponies = ["twilight sparkle","applejack","rarity","pinkie pie","rainbow dash","fluttershy"]
parentdir = Path(__file__).resolve().parents[1]
with open(os.path.join(parentdir, 'data', 'stopwords.txt'), "r") as stop:
    stopwords = stop.read()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d',required=True, dest='d', help="clean dialog abs path")
    parser.add_argument('-o', required=True, dest='o', help="output file abs path")
    args=parser.parse_args()
    if not os.path.dirname(args.o) == "":
        os.makedirs(os.path.dirname(args.o), exist_ok=True)
    result = get_speech_frequency(args.d)
    with open(args.o, 'w') as o:
        json.dump(result, o)

def get_speech_frequency(fname):
    result = {}
    for pony in ponies:
        result[pony]={}
    with open(fname, 'r') as d:
        reader = csv.DictReader(d)
        for row in reader:
            if row["pony"].lower() in ponies:
                text = row["dialog"]
                #replace punctuation
                for punc in punctuation:
                    text = text.replace(punc, " ")
                words = text.split()
                for word in words:
                    if not word.isalpha():
                        continue
                    word = word.lower()
                    if word in stopwords:
                        continue
                    if word not in result[row["pony"].lower()].keys():
                        result[row["pony"].lower()][word] = 1
                    else:
                        result[row["pony"].lower()][word] += 1
    # sort and remove rare words <5 occurrences
    final={}
    for pony in ponies:
        final[pony] = {}
    for pony in ponies:
        for entry in result[pony]:
            num = 0
            for p in ponies:
                if entry in result[p].keys():
                    num += result[p][entry]
            if num >= 5:
                final[pony][entry] = result[pony][entry] 
    return final
    

    



if __name__=="__main__":
    main()
import json
import argparse
import os, sys
import csv

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i',required=True, dest='i', help="input file path")
    parser.add_argument('-o', required=True, dest='o', help="output file path")
    args=parser.parse_args()
    if not os.path.dirname(args.o) == "":
        os.makedirs(os.path.dirname(args.o), exist_ok=True)
    output = get_interactions(args.i)
    with open(args.o, 'w') as o:
        json.dump(output, o)
    


def get_interactions(fpath):
    interactions = {}
    speakers = {}
    invalid_speakers = []
    with open(fpath, "r") as f:
        reader = csv.DictReader(f)
        #find ponies not in top 101 speakers:
        for row in reader:
            if is_valid_pony(row["pony"].lower()):
                if row["pony"].lower() not in speakers.keys():
                    speakers[row["pony"].lower()] = 1
                else:
                    speakers[row["pony"].lower()] += 1
        if len(speakers) >= 101:
            speakers = dict(sorted(speakers.items(), key=lambda item: item[1], reverse=True))
            num = 0
            for key, value in speakers.items():
                if num < 101:
                    num += 1
                    continue
                else:
                    invalid_speakers.append(key)
        #tracker keeps track of last pony that spoke, becomes "" if last speaker was invalid
        tracker = ""
        #episode keeps track of episode on last iteration
        episode = ""
        f.seek(0)
        for row in reader:
            name = row["pony"].lower().strip()
            #if speaker is not valid continue and set tracker to ""
            if (not is_valid_pony(name)) or (name in invalid_speakers):
                tracker = ""
                episode = row["title"]
                continue
            #pony cant speak to itself
            if name == tracker:
                episode = row["title"]
                continue
            #if name not in interaction dict, add it (could still be empty afterwards)
            if name not in interactions.keys():
                interactions[name] = {}
            #episode check - new chain if new episode
            if episode != "" and row["title"] != episode:
                tracker = name
                episode = row["title"]
                continue
            #if last speaker was valid, and this speaker is valid, increment interaction dict 
            if tracker != "":
                if name not in interactions[tracker].keys():
                    interactions[tracker][name] = 1
                else:
                    interactions[tracker][name] += 1
                if tracker not in interactions[name].keys():
                    interactions[name][tracker] = 1
                else:
                    interactions[name][tracker] += 1
            tracker = name
            episode = row["title"]
    return interactions

def is_valid_pony(name):
    if "and" in name:
        return False
    elif "other" in name:
        return False
    elif "ponies" in name:
        return False 
    elif "all" in name:
        return False
    return True

if __name__=="__main__":
    main()
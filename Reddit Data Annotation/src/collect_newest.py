import requests
import os, sys
import json
import argparse

parser = argparse.ArgumentParser(description="Find relationships")
parser.add_argument('-s',required=True, dest='s', help="subreddit name")
parser.add_argument('-o', required=True, dest='o', help="output file relative path")
args=parser.parse_args()
if not os.path.dirname(args.o) == "":
    os.makedirs(os.path.dirname(args.o), exist_ok=True)

def main():
    subreddit = args.s
    r = requests.get(f"https://www.reddit.com/{subreddit}/new.json?limit=100", headers = {"User-Agent": 'avg-post-length:0.0.01'})
    data = r.json()['data']['children']
    with open(args.o, 'w') as o:
        for post in data:
            o.write(json.dumps(post)+'\n')


if __name__=="__main__":
    main()
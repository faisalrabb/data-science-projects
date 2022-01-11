import requests
import os, sys
import json
import argparse
import csv
import random

parser = argparse.ArgumentParser(description="Find relationships")
parser.add_argument('-o', required=True, dest='o', help="output file relative path")
parser.add_argument('json_file')
parser.add_argument('num_posts')
args=parser.parse_args()
#print(args.o)
#print(args.json_file)
#print(args.num_posts)

if not os.path.dirname(args.o) == "":
    os.makedirs(os.path.dirname(args.o), exist_ok=True)


def main():
    posts=[]
    with open(args.json_file, 'r') as js:
        for row in js:
            data = json.loads(row)
            posts.append(data)

    with open(args.o, 'w') as o:
        writer = csv.DictWriter(o, fieldnames=["Name", "title", "coding"], dialect='excel-tab')
        writer.writeheader()
        post_data=[]
        for post in posts:
            post_data.append({'Name': post["data"]["name"], 'title': post["data"]["title"], 'coding': ""})
        if int(args.num_posts) < len(post_data) and int(args.num_posts)>0:
            writer.writerows(random.sample(post_data, int(args.num_posts)))
        else:
            writer.writerows(post_data)

    

if __name__ == "__main__":
    main()

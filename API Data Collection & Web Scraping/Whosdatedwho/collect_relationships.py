import os, sys
import json
import requests
from bs4 import BeautifulSoup as bs
import argparse

BASE_URL = 'https://www.whosdatedwho.com/dating/'



def main():
    parser = argparse.ArgumentParser(description="Find relationships")
    parser.add_argument('-c',required=True, dest='c', help="config file relative path")
    parser.add_argument('-o', required=True, dest='o', help="output file relative path")
    args=parser.parse_args()
    with open(args.c, 'r') as c:
        config = json.load(c)
        c.close()
    cache = config["cache_dir"]
    if not os.path.exists(cache):
        os.makedirs(cache)
    ###CREATE UNIQUE FILENAME TO WRITE TO AND CHECK --OR-- 1 FILE PER PERSON 
    for person in config["target_people"]:
        filename = cache+"/"+person.replace(" ", "_")+".txt"
        if not os.path.exists(filename):
            scrape(person, filename)
    #FOR EACH, CHECK THAT FILE EXISTS, IF NOT, SCRAPE, MOVE ON TO NEXT STEP USING CACHED DOCUMENTS ! 
    get_relationships(config["target_people"], args.o, cache)

                    

def get_relationships(persons, output_file, cache):
    output = {}
    #for each, get info from cache, add to dict, dump dict to output file
    for person in persons:
        filename = filename = cache+"/"+person.replace(" ", "_")+".txt"
        with open(filename, 'r') as f:
            dated = [] 
            data = json.load(f)
            # extract relationships, add to dated
            for d in data["itemListElement"]:
                dated.append(d["item"]["name"])
            output[person] = dated
    with open(output_file, 'w') as o:
        json.dump(output, o)


def scrape(person, filename):
    data = get_json(person)
    with open(filename, 'w+') as cch:
        json.dump(data, cch)
        cch.close()
            
def get_json(person):
    person_url = BASE_URL+person
    r=requests.get(person_url)
    soup = bs(r.content, 'html.parser')
    data = json.loads(soup.find('script', type='application/ld+json').text)
    return data

if __name__=='__main__':
    main() 
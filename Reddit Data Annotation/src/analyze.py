import csv
import argparse
import os, sys
import json

parser = argparse.ArgumentParser(description="Find relationships")
parser.add_argument('-o', required=False, dest='o', help="output file relative path", default="")
parser.add_argument('-i', required=True, dest='i', help="input file relative path")
args=parser.parse_args()

if args.o != "":
    if not os.path.dirname(args.o) == "":
        os.makedirs(os.path.dirname(args.o), exist_ok=True)

def main() :

    with open(args.i, 'r') as input_file:
        frequency = {'course-related': 0, 'food-related': 0, 'residence-related':0,'other':0}
        reader = csv.reader(input_file, dialect='excel-tab')
        for line in reader:
            code = line[2]
            if code=='c':
                frequency['course-related']+=1
            elif code == 'o':
                frequency['other']+=1 
            elif code =='r':
                frequency['residence-related']+= 1
            elif code =='f':
                frequency['food-related']+=1
            else:
                frequency['other'] += 1
    if args.o=="":
        print(json.dumps(frequency, indent=4))
    else:
        with open(args.o, 'w') as o:
            o.write(json.dumps(frequency, indent=4))

if __name__=="__main__":
    main()
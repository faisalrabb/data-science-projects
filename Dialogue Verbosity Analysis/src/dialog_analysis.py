import sys
import csv
import json

def main(): 
    output_file = sys.argv[2]
    input_file = sys.argv[3]
    total = 0
    twilight = 0
    applejack = 0
    rarity = 0
    pinkie = 0
    rainbow = 0
    fluttershy = 0
    with open(input_file, newline='') as data: 
        reader = csv.DictReader(data)
        for row in reader: 
            total += 1
            speaker = row['pony']
            speaker = speaker.lower()
            if speaker == 'twilight sparkle':
                twilight += 1
            elif speaker == 'applejack':
                applejack += 1
            elif speaker == 'rarity':
                rarity += 1
            elif speaker == 'pinkie pie':
                pinkie += 1
            elif speaker == 'rainbow dash':
                rainbow += 1
            elif speaker == 'fluttershy':
                fluttershy += 1

    count_dict = {'twilight sparkle': twilight, 'applejack': applejack, 'rarity': rarity, 'pinkie pie': pinkie, 'rainbow dash': rainbow, 'fluttershy': fluttershy}
    verbosity_dict ={'twilight sparkle': round(twilight/total,2), 'applejack': round(applejack/total,2), 'rarity': round(rarity/total,2), 'pinkie pie': round(pinkie/total,2), 'rainbow dash': round(rainbow/total,2), 'fluttershy': round(fluttershy/total,2)}
    big_dict = {'count': count_dict, 'verbosity': verbosity_dict}

    #print(twilight/total + applejack/total + rarity/total+pinkie/total+rainbow/total+fluttershy/total)
    with open(output_file, 'w') as of: 
        json.dump(big_dict, of)
    
main() 

    




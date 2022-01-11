import argparse
import json
import datetime
import dateutil.parser

def main():
    parser = argparse.ArgumentParser(description="Clean JSON data")
    parser.add_argument('-i',required=True, dest='i', help="input file relative path")
    parser.add_argument('-o', required=True, dest='o', help="output file relative path")
    args=parser.parse_args()
    with open(args.i, 'r') as ifile:
        cleaned_data = cleaner(ifile.read())
    with open(args.o, 'w') as ofile:
        json.dump(cleaned_data, ofile)

def cleaner(raw_data):
    cleaned_data=[]
    for line in raw_data.splitlines():
        try:
            post = json.loads(line)
        except:
            #print('invalid json dict')
            continue
        if type(post) is not dict:
            #print('not dict')
            continue
        if "title" not in post and "title_text" not in post:
            #print('cond 1')
            continue
        if not follows_iso(post['createdAt']):
            #print('iso')
            continue
        if type(post['author']) is not str or len(post['author']) < 1 or post['author'] == 'N/A':
            continue
        if "total_count" in post:
            try:
                if type(post['total_count']) in [str, float, int]:
                    post['total_count'] = int(post['total_count'])
                else:
                    raise Exception("Total count can't be parsed to int")
            except:
                continue
        if "tags" in post:
            post['tags'] = format_tags(post['tags'])
        post['createdAt'] = convert_to_utc(post['createdAt'])
        cleaned_data.append(post)
    return cleaned_data


def format_tags(tags):
    result = []
    for tag in tags:
        x = tag.split()
        for word in x:
            result.append(word)
    return result

def follows_iso(date_string):
    try:
        dt = dateutil.parser.isoparse(date_string)
    except ValueError:
        return False
    return True

def convert_to_utc(date_string):
    dt = dateutil.parser.isoparse(date_string)
    timestamp = dt.replace(tzinfo=datetime.timezone.utc)
    converted_dt = timestamp.isoformat()
    return converted_dt

if __name__=='__main__':
    main()
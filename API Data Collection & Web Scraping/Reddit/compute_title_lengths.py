import json
import sys, os

filename = sys.argv[1]
#print(filename)

def main():
    total_num=0
    total_posts=0
    with open(filename, 'r') as f:
        for line in f:
            jdict = json.loads(line)
            post_title = jdict['data']['title']
            total_num+= len(post_title)
            total_posts+=1
    f.close()
    if total_posts>0:
        print(round(total_num/total_posts,2))


if __name__=='__main__':
    main()


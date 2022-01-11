import requests
import json
import os, sys, time

top_10_subs = ['funny', 'AskReddit', 'gaming', 'aww', 'pics', 'Music', 'science', 'worldnews', 'videos', 'todayilearned']
top_10_posts = ['AskReddit', 'memes', 'politics', 'nfl', 'nba', 'wallstreetbets', 'teenagers', 'PublicFreakout', 'leagueoflegends', 'unpopularopinion']
client_id='cmBn_I8y1v7gVtTfWWgvjg'
secret = 'xJbZ1UJvWCvhH3o8HBCZj-QvTy9QRQ'
api_url = 'https://reddit.com'
username = 'comp598_bot'
password = 'comp598comp598'



def main():
    auth = requests.auth.HTTPBasicAuth(client_id, secret)
    data = {'grant_type': 'password','username': username,'password': password, 'redirect_uri': 'http://www.example.com/unused/redirect/uri'}
    headers={'User-Agent': 'avg_post_length/0.0.1'}
    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
    TOKEN = res.json()['access_token']
    print(TOKEN)
    headers['Authorization'] = f"bearer {TOKEN}"
    write_posts(headers)


def write_posts(headers):
    with open('sample1.json', 'w') as s1:
        for sub in top_10_subs:
            time.sleep(1)
            r=requests.get(f'https://oauth.reddit.com/r/{sub}/new?limit=100', headers=headers)
            for post in r.json()['data']['children']:
                post_str = json.dumps(post)
                s1.write(post_str+'\n')
    s1.close()
    with open('sample2.json', 'w') as s2:
        for sub in top_10_posts:
            time.sleep(1)
            r=requests.get(f'https://oauth.reddit.com/r/{sub}/new?limit=100', headers=headers)
            for post in r.json()['data']['children']:
                post_str = json.dumps(post)
                s2.write(post_str+'\n')
    s2.close()
        
if __name__=='__main__':
    main()

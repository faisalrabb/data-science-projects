import requests
import os
import json
import dateutil.parser
import time
import sys
from pathlib import Path
parentdir = Path(__file__).parents[0]
sys.path.append(parentdir)
sys.path.append('.')


# Import settings from .env file
if os.path.exists(".env"):
    print("Importing environment from .env file")
    for line in open(".env"):
        var = line.strip().split("=")
        os.environ[var[0]] = var[1]
else:
    sys.exit("ERROR: NO .env file")

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")

class GetTweets:

    def main(self, start_time, end_time):
        url = self.create_search_url()
        
        json_response = self.connect_to_endpoint(url, start_time, end_time)
        self.output(json_response, start_time, 0)
        id = 1
        while "next_token" in json_response["meta"]:
            next_token = json_response["meta"]["next_token"]
            json_response = self.connect_to_endpoint(url, start_time, end_time, next_token)
            self.output(json_response, start_time, id)
            id += 1
            time.sleep(2)
        # print(json.dumps(json_response, indent=4, sort_keys=True))

    
    def create_params(self, start_time, end_time, next_token):
        #Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
        # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields

        # No Time To Die Query: (#NoTimeToDie OR #NoTimeToDieMovie OR #NoTimeToDie2021 OR "No Time To Die")
        # Dune Query: ()

        query_params = {'query': '(#Dune OR #DuneMovie OR "Dune") lang:en -is:retweet -is:reply',
            'tweet.fields': 'author_id,lang,possibly_sensitive,geo,public_metrics,created_at', 
            'user.fields' : 'username,description,verified',
            "max_results" : 100,
            'start_time': start_time,

        }

        if next_token:
            query_params["next_token"] = next_token
        if end_time:
            query_params["end_time"] = end_time

        return query_params

    def create_search_url(self):
        search_url = "https://api.twitter.com/2/tweets/search/recent"

        return search_url

    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {bearer_token}"
        r.headers["User-Agent"] = "v2RecentSearchPython"
        return r


    def connect_to_endpoint(self, url, start_time, end_time, next_token = None):
        response = requests.request("GET", url, auth=self.bearer_oauth, params=self.create_params(start_time, end_time, next_token))
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()
    
    def output(self, data, date, id):
        with open('{}_{}.json'.format(dateutil.parser.isoparse(date).date(), id), 'w') as f:
            json.dump(data, f, indent=4)


# Initial Start Date For No TIme tO Die
# start_time = "2021-12-01T00:00:14.000Z"
# end_time = "2021-12-05T23:59:14.000Z"

# Initial Start Date For Dune
# start_time = "2021-12-03T00:00:14.000Z"
# end_time = "2021-12-06T23:59:14.000Z"

if __name__ == "__main__":
    start_time = "2021-12-03T00:00:14.000Z"
    end_time = "2021-12-06T23:59:14.000Z"
    if end_time:
        GetTweets().main(start_time=start_time, end_time=end_time)
    else:
        GetTweets().main(start_time=start_time)
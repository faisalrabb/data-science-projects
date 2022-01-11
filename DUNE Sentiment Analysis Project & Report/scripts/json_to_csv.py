import pandas as pd
import os
import json
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

class JSONToCSV:

    def main(self, date, start_index, end_index, movie):
        data = []
        for i in range(start_index, end_index + 1):
            data.append(self.add_json("{}_{}".format(date, i), movie))
        
        df = self.convert_to_df(data)
        self.output(df, movie)


    def add_json(self, json_name, movie):
        with open("data/{}/{}.json".format(movie, json_name)) as f:
            data = json.load(f)
            return data

    def convert_to_df(self, data):
        df = pd.DataFrame(columns=["lang", "sensitive", "retweet", "reply", "likes", "quote", "created", "text", "id", "author_id"])
        for obj in data:
            for tweet in obj["data"]:
                df = df.append(
                    {
                        "lang": tweet["lang"], 
                        "sensitive": tweet["possibly_sensitive"],
                        "retweet": tweet["public_metrics"]["retweet_count"],
                        "reply": tweet["public_metrics"]["reply_count"],
                        "likes": tweet["public_metrics"]["like_count"],
                        "quote": tweet["public_metrics"]["quote_count"],
                        "created": tweet["created_at"],
                        "text": tweet["text"],
                        "id": tweet["id"],
                        "author_id": tweet["author_id"]
                    },
                    ignore_index=True
                )
        return df

    def output(self, dataframe, movie):
        dataframe.to_csv("{}_data.csv".format(movie))
        
            
if __name__ == "__main__":
    JSONToCSV().main("2021-12-03", 0, 87, "Dune")
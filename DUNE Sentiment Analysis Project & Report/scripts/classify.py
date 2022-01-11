import csv
import os

categories = ["review", "theatre/cinema mention", "actors/characters", "awards/nomination","cinematography/videography", "soundtrack or sound quality", "book", "other"]
prompt1 = "Select topic (1: review, 2: theatre/cinema, 3: actors/characters, 4: awards/nomination, 5:cinematography/videography, 6: soundtrack, 7:book, 8: other)"
prompt2 = "Select sentiment: (p=positive, n=negative, e=neutral)"
def main():
    val = os.system("touch ../data/Dune_1000_annotated.csv")
    with open("../data/Dune_1000.csv", "r") as i:
        reader=csv.DictReader(i)
        with open("../data/Dune_1000_annotated.csv", 'a') as o:
            writer = csv.DictWriter(o, fieldnames=reader.fieldnames)
            i=1
            for row in reader:
                if i==1 and row["text"] != "":
                    writer.writeheader()
                i+=0
                print(f"tweet #{i}")
                if row["text"] == "":
                    continue
                print(row["text"])
                try:
                    topic = int(input(prompt1))
                except:
                    topic = int(input(prompt1))
                while topic < 1 or topic > 8:
                    topic = int(input(prompt1))
                sentiment = input(prompt2)
                while sentiment not in  ["p","n", "e"]:
                    sentiment = input(prompt2)
                row["topic"] = categories[topic-1]
                if sentiment == "p":
                    row["sentiment"] = "positive"
                if sentiment == "n":
                    row["sentiment"] = "negative"
                if sentiment == "e":
                    row["sentiment"] = "neutral"
                writer.writerow(row)
                print("______________________")
            print("done!")


if __name__=="__main__":
    main()
import pandas as pd
import sys
from pathlib import Path
parentdir = Path(__file__).parents[0]
sys.path.append(parentdir)
sys.path.append('.')

class RandomSelect:

    def main(self, csv, movie, n):
        df = pd.read_csv(csv)

        

        self.output(df.sample(n), movie, n)

    def output(self, df, movie, n):
        df.to_csv("{}_sample_{}.csv".format(movie, n))
        
            
if __name__ == "__main__":
    RandomSelect().main("data/Dune_data.csv", "Dune", 200)
    RandomSelect().main("data/Dune_data.csv", "Dune", 1000)
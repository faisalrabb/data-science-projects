import pandas as pd

df = pd.read_csv("data/Dune_sample_200_edited.csv")

print(df['Topics'].value_counts())
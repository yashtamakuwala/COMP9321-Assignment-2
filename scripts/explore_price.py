import os
import pandas as pd

root = os.path.abspath(os.curdir)
path_of_data = os.path.join(root, 'data/listings_clean.csv')
df = pd.read_csv(path_of_data)

# Take rating only
columns = ['LGA', 'price']
df = df[columns]

df = df.groupby('LGA').mean().reset_index().sort_values('LGA')
print(df)

import os
import pandas as pd

root = os.path.abspath(os.curdir)
path_of_data = os.path.join(root, 'data/lga_postcode_map.csv')
df = pd.read_csv(path_of_data)

# Remove non-NSW rows
df = df[df['State'] == 'New South Wales']

# Remove State column
df = df.drop(df.columns[0], axis=1)

# Rename 1st column to LGA
df = df.rename({df.columns[0]: 'LGA'}, axis=1)

# export
df.to_csv('data/lga_postcode_map_cleaned.csv', index=False)

import os
import pandas as pd

root = os.path.abspath(os.curdir)
path_of_data = os.path.join(root, 'data/crime_raw.csv')
df = pd.read_csv(path_of_data)

# Remove useless columns
df = df.drop(df.columns[1:3], axis=1)

# Remove the last 4 rows
df = df.iloc[:-4]

month_columns = df.columns[1:]
astype_map = {column : int for column in month_columns}
df = df.astype(astype_map)

# export
df.to_csv('data/crime_clean.csv', index=False)

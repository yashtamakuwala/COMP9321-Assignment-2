import os
import pandas as pd

os.chdir("..")
os.chdir("..")
root = os.path.abspath(os.curdir)
path_of_data = os.path.join(root, 'data/crime_raw.csv')
df = pd.read_csv(path_of_data)

# Remove 1st column
df = df.drop([df.columns[0],df.columns[2],df.columns[3]],axis = 1)

# Remove the last 4 rows
df = df.iloc[:-4]
print(df)

month_columns = df.columns[1:]
astype_map = {column : int for column in month_columns}
df = df.astype(astype_map)

print(df)

# export
df.to_csv('data/crime_cleaned.csv', index=True)
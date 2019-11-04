import os
import pandas as pd

os.chdir("..")
root = os.path.abspath(os.curdir)
path_of_data = os.path.join(root, 'data/listings.csv')
df = pd.read_csv(path_of_data)
print(df)
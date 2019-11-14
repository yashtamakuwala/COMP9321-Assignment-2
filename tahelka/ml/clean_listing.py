import os
import pandas as pd
import copy
import math
import numpy as np
from sklearn.metrics import confusion_matrix 
from sklearn.model_selection import train_test_split

os.chdir("..")
os.chdir("..")
root = os.path.abspath(os.curdir)
path_of_data = os.path.join(root, 'data/listings.csv')
path_of_data2 = os.path.join(root, 'data/crime_cleaned.csv')
df = pd.read_csv(path_of_data)
dfc = pd.read_csv(path_of_data2)

# Keep required columns
required_columns = ["price", "beds", "accommodates", "property_type","room_type", "city"]
df = df[required_columns]

# Remove NaN

# Convert beds to integer
df = df.astype({'beds' : int})
#df = df.merge(dfc,on="city", how = "left")

# Clean city values
crime_cities = dfc["LGA"].apply(lambda x : x.lower()).unique()
df = df[df['city'].isin((crime_cities))]

# export
df.to_csv('data/cleaned_listings.csv', index=True)
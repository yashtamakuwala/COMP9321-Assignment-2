import os
import pandas as pd

os.chdir("..")
os.chdir("..")
root = os.path.abspath(os.curdir)
path_of_data = os.path.join(root, 'data/listings.csv')
path_of_data2 = os.path.join(root, 'data/crime_cleaned.csv')
df = pd.read_csv(path_of_data)
dfc = pd.read_csv(path_of_data2)

# Keep required columns
required_columns = ["price", "beds", "accommodates", "property_type","room_type",
                    "city", "review_scores_rating"]
df = df[required_columns]

# Rename review column
df = df.rename({'review_scores_rating': 'rating'}, axis=1)

# Remove NaN
df = df.dropna()

# Clean city values
df['city'] = df['city'].apply(lambda x: x.strip())
crime_cities = dfc["LGA"].unique()
df = df[df['city'].isin((crime_cities))]

# Convert beds and review to integer
df = df.astype({'beds' : int, 'rating': int})

# Convert price to int
df['price'] = df['price'].apply(lambda x: float(x.replace(',','').replace('$','')))
df = df.astype({'price': int})

# export
df.to_csv('data/listings_cleaned.csv', index=True)
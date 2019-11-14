import os
import pandas as pd

def normalize_price(price_raw):
    return int(float(price_raw.replace(',','').replace('$','')))

root = os.path.abspath(os.curdir)
listing_path = os.path.join(root, 'data/listings.csv')
clean_crime_path = os.path.join(root, 'data/crime_cleaned.csv')
df = pd.read_csv(listing_path)
dfc = pd.read_csv(clean_crime_path)

# Keep required columns
required_columns = ['city', 'beds', 'accommodates', 'property_type',
                    'room_type', 'price', 'review_scores_rating']
df = df[required_columns]

# Rename review column
df = df.rename({'review_scores_rating': 'rating'}, axis=1)

# Remove rows with NaN ML attributes
ml_columns = required_columns[:-1]
df= df.dropna(subset=ml_columns)

# Clean city values
df['city'] = df['city'].apply(lambda x: x.strip())
crime_cities = dfc["LGA"].unique()
df = df[df['city'].isin((crime_cities))]

# Convert beds to integer
df = df.astype({'beds' : int})

# Normalize price
df['price'] = df['price'].apply(normalize_price)

print(df)
print(len(df))

# export
df.to_csv('data/listings_cleaned.csv', index=False)

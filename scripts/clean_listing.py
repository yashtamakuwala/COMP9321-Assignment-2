import os
import pandas as pd

buckets = [40, 50, 60, 70, 80, 90, 100, 115, 125, 140, 150, 175, 200, 210,
           250, 300, 400, 600]

def normalize_price(price_raw):
    return int(float(price_raw.replace(',','').replace('$','')))

# Load airbnb dataset
root = os.path.abspath(os.curdir)
listing_path = os.path.join(root, 'data/listings.csv')
df = pd.read_csv(listing_path)

# Rename columns
map = {'review_scores_rating': 'rating', 'neighbourhood_cleansed': 'LGA_2011'}
df = df.rename(map, axis=1)

# Keep required columns
required_columns = ['LGA_2011', 'beds', 'accommodates', 'property_type',
                    'room_type', 'price', 'rating']
df = df[required_columns]

# Remove rows used for ML with NaN
ml_columns = required_columns[:-1]
df = df.dropna(subset=ml_columns)

# Normalize LGA
df['LGA_2011'] = df['LGA_2011'].str.replace('Ku-Ring-Gai', 'Ku-ring-gai')
df['LGA_2011'] = df['LGA_2011'].str.replace('City Of Kogarah', 'Kogarah')

# Convert LGA to 2016
conversion_path = os.path.join(root, 'data/lga_conversion_clean.csv')
dfco = pd.read_csv(conversion_path)
df = df.merge(dfco, how='left', left_on='LGA_2011', right_on='LGA_NAME_2011')
df = df.drop(['LGA_2011', 'LGA_NAME_2011'], axis=1)
df = df.rename({'LGA_NAME_2016': 'LGA'}, axis=1)

# Convert beds to integer
df = df.astype({'beds' : int})

# Remove rows with esoteric property type
s = df['property_type'].value_counts()
major_types = s[s >= 15].index
df = df[df['property_type'].isin(major_types)]

# Normalize price
df['price'] = df['price'].apply(normalize_price)

# export
df.to_csv('data/listings_clean.csv', index=False)

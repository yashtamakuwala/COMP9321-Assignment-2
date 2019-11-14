import os
import pandas as pd

buckets = [40, 50, 60, 70, 80, 90, 100, 115, 125, 140, 150, 175, 200, 210,
           250, 300, 400, 600]

def normalize_price(price_raw):
    return int(float(price_raw.replace(',','').replace('$','')))

def decide_bucket(price):
    if price <= buckets[0]:
        return f'<= ${buckets[0]}'

    for index, bucket in enumerate(buckets[1:]):
        if price > bucket:
            continue

        return f'${buckets[index - 1] + 1} - ${bucket}'

    return f'> ${buckets[-1]}'

# Load airbnb dataset
root = os.path.abspath(os.curdir)
listing_path = os.path.join(root, 'data/listings.csv')
df = pd.read_csv(listing_path)

# Rename columns
map = {'review_scores_rating': 'rating', 'neighbourhood_cleansed': 'LGA'}
df = df.rename(map, axis=1)

# Keep required columns
required_columns = ['LGA', 'beds', 'accommodates', 'property_type',
                    'room_type', 'price', 'rating']
df = df[required_columns]

# Remove rows used for ML with NaN
ml_columns = required_columns[:-1]
df = df.dropna(subset=ml_columns)

# Normalize LGA
df['LGA'] = df['LGA'].str.replace('Ku-Ring-Gai', 'Ku-ring-gai')
df['LGA'] = df['LGA'].str.replace('City Of Kogarah', 'Kogarah')

# Convert beds to integer
df = df.astype({'beds' : int})

# Remove rows with esoteric property type
s = df['property_type'].value_counts()
major_types = s[s >= 15].index
df = df[df['property_type'].isin(major_types)]

# Normalize price
df['price'] = df['price'].apply(normalize_price)

# Put price to buckets
df['price_range'] = df['price'].apply(decide_bucket)

# export
df.to_csv('data/listings_cleaned.csv', index=False)

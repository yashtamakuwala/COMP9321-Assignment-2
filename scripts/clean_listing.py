import os
import pandas as pd

def normalize_price(price_raw):
    return int(float(price_raw.replace(',','').replace('$','')))

def decide_bucket(price):
    buckets = [45, 50, 60, 70, 80, 90, 100, 115, 125, 140, 150, 175, 200, 210,
               250, 300, 400, 600]
    if price <= buckets[0]:
        return f'<= ${buckets[0]}'

    for index, bucket in enumerate(buckets):
        if price > bucket:
            continue

        return f'${buckets[index - 1] + 1} - ${bucket}'

    return f'> ${buckets[-1]}'

    if price <= buckets[0]:
        return f'<= ${buckets[0]}'

    for index, bucket in enumerate(buckets):
        if price > bucket:
            continue

        return f'${buckets[index - 1]} - ${bucket}'

    return f'> ${buckets[-1]}'

# Load airbnb dataset
root = os.path.abspath(os.curdir)
listing_path = os.path.join(root, 'data/listings.csv')
df = pd.read_csv(listing_path)

# Keep required columns
required_columns = ['zipcode', 'beds', 'accommodates', 'property_type',
                    'room_type', 'price', 'review_scores_rating']
df = df[required_columns]

# Rename review column
df = df.rename({'review_scores_rating': 'rating'}, axis=1)

# Remove rows with NaN ML attributes
ml_columns = required_columns[:-1]
df = df.dropna(subset=ml_columns)

# Clean zipcode
df['zipcode'] = df['zipcode'].str.replace(r'[^0-9.]', '') # Remove non-numeric
df['zipcode'] = df['zipcode'].str.strip()                 # Strip
df = df.dropna(subset=['zipcode'])                        # Dropna
df = df.astype({'zipcode': int})                          # Convert to int

# Map zipcode to LGA values
lga_postcode_map_path = os.path.join(root, 'data/lga_postcode_map_cleaned.csv')
dfm = pd.read_csv(lga_postcode_map_path)
df = df.merge(dfm, left_on='zipcode', right_on='Postcode')
df = df.drop(['zipcode'], axis=1)

# Take only LGA in crime datasets
crime_path = os.path.join(root, 'data/crime_cleaned.csv')
dfc = pd.read_csv(crime_path)
crime_lgas = dfc['LGA'].unique()
df = df[df['LGA'].isin(crime_lgas)]

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

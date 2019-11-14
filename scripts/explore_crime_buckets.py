import os
import pandas as pd

def decide_bucket(mean_crime_count):
    buckets = [250, 500, 1000, 1500]
    levels = ['Very Low', 'Low', 'Average', 'High', 'Very High']
    if mean_crime_count <= buckets[0]:
        return levels[0]

    for index, bucket in enumerate(buckets[1:]):
        if mean_crime_count > bucket:
            continue

        return levels[index + 1]

    return levels[-1]

root = os.path.abspath(os.curdir)
path_of_data = os.path.join(root, 'data/crime_cleaned.csv')
dfc = pd.read_csv(path_of_data)

# Get monthly mean of crime count
month_columns = dfc.columns[1:]
dfc['mean_crime_count'] = dfc[month_columns].mean(axis='columns')

# Drop month columns
dfc = dfc.drop(month_columns, axis=1)

# Group by LGA
dfc = dfc.groupby(['LGA']).sum().reset_index()

# Merge with listing
listings_path = os.path.join(root, 'data/listings_cleaned.csv')
dfl = pd.read_csv(listings_path)

dfl = dfl.merge(dfc, on='LGA')
airbnb_cities = dfl['LGA'].unique()

dfc = dfc[dfc['LGA'].isin(airbnb_cities)]

dfc['crime_level'] = dfc['mean_crime_count'].apply(decide_bucket)

print(dfc)

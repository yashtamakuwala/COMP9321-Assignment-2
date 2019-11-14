import os
import pandas as pd
import numpy as np

def decide_bucket(rate):
    buckets = [2, 4, 6, 8]
    levels = ['Far Below Average', 'Below Average', 'Average', 'Above Average',
              'Far Above Average']
    if rate <= buckets[0]:
        return levels[0]

    for index, bucket in enumerate(buckets[1:]):
        if rate > bucket:
            continue

        return levels[index + 1]

    return levels[-1]

root = os.path.abspath(os.curdir)
path_of_data = os.path.join(root, 'data/unemployment_clean.csv')
dfu = pd.read_csv(path_of_data)

# Get monthly mean of unemployment rate
month_columns = dfu.columns[1:]
dfu['mean_unemp_rate'] = dfu[month_columns].mean(axis='columns')

# Drop month columns
dfu = dfu.drop(month_columns, axis=1)

# Filter according to LGA in listing
listings_path = os.path.join(root, 'data/listings_clean.csv')
dfl = pd.read_csv(listings_path)

airbnb_cities = dfl['LGA'].unique()

dfu = dfu[dfu['LGA'].isin(airbnb_cities)]

print(dfu['mean_unemp_rate'].agg(np.mean))

dfu['unemployment_rate_level'] = dfu['mean_unemp_rate'].apply(decide_bucket)

print(dfu)

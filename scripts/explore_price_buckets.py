import os
import pandas as pd

def decide_bucket(price):
    buckets = [40, 60, 80, 100, 125, 150, 200, 250, 400, 600]
    if price <= buckets[0]:
        return f'<= ${buckets[0]}'

    for index, bucket in enumerate(buckets[1:]):
        if price > bucket:
            continue

        return f'${buckets[index] + 1} - ${bucket}'

    return f'> ${buckets[-1]}'

root = os.path.abspath(os.curdir)
path_of_data = os.path.join(root, 'data/listings_clean.csv')
df = pd.read_csv(path_of_data)

df = df.sort_values('price')
df['bucket'] = df['price'].apply(decide_bucket)
print(df['bucket'].value_counts()[:50])

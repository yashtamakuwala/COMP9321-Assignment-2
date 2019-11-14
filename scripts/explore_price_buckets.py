import os
import pandas as pd

def get_bucket(price):
    if price >= 500:
        return ">= $500"
    if 300 <= price and price < 500:
        return "$300 - $500"
    if 200 <= price and price < 300:
        return "$200 - $300"
    if price < 40:
        return "< $40"

    return f"${price // 20 * 20} - ${price // 20 * 20 + 20}"

os.chdir("..")
os.chdir("..")
root = os.path.abspath(os.curdir)
path_of_data = os.path.join(root, 'data/listings_cleaned.csv')
df = pd.read_csv(path_of_data)

df = df.sort_values('price')
df['bucket'] = df['price'].apply(get_bucket)
print(df['bucket'].value_counts()[:50])


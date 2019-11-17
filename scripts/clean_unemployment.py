import os
import pandas as pd

root = os.path.abspath(os.curdir)
path_of_data = os.path.join(root, 'data/unemployment_raw.csv')
df = pd.read_csv(path_of_data)

# convert LGA Code to int
df = df.astype({'LGA Code': int})

# Take only NSW LGAs & unemployment rate
df = df[df['LGA Code'] < 20000]
df = df[df['Data item'] == 'Smoothed unemployment rate (%)']

# Remove useless columns
df = df.drop(['Data item', 'LGA Code'], axis=1)

# Rename LGA column
df = df.rename({'Local Government Area (LGA)': 'LGA'}, axis=1)

# Normalize LGA
df['LGA'] = df['LGA'].str.replace(' \([A-Z]+\)', '')

# export
df.to_csv('data/unemployment_clean.csv', index=False)

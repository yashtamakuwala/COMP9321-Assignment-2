import os
import pandas as pd

root = os.path.abspath(os.curdir)
path_of_data = os.path.join(root, 'data/lga_conversion_raw.csv')
df = pd.read_csv(path_of_data)

# convert LGA Code 2011 to int
df = df.astype({'LGA_CODE_2011': int})

# Take only NSW LGAs
df = df[df['LGA_CODE_2011'] < 20000]

# Take only percentage >= 50
df = df[df['PERCENTAGE'] >= 50]

# Drop unneeded columns
df = df.drop(['LGA_CODE_2011', 'LGA_CODE_2016', 'RATIO'], axis=1)

# Normalize names
df['LGA_NAME_2011'] = df['LGA_NAME_2011'].str.replace(' \([A-Z]+\)', '')
df['LGA_NAME_2016'] = df['LGA_NAME_2016'].str.replace(' \([A-Z]+\)', '')

# export
df.to_csv('data/lga_conversion_clean.csv', index=False)

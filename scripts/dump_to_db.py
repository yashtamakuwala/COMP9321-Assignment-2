from alchemy import Engine
from alchemy import Session
from tahelka.models.Property import Property
import pandas as pd
from sqlalchemy.types import Integer, String
import os

# Load CSV
root = os.path.abspath(os.curdir)
path_of_data = os.path.join(root, 'data/listings_clean.csv')
df = pd.read_csv(path_of_data)

# rename columns
column_mapping = {
    'accommodates' : 'guest_count',
    'beds' : 'bed_count',
    'LGA' : 'lga'
}
df = df.rename(column_mapping, axis=1)

# Set column type
dtype_mapping = {
    'id': Integer(),
    'lga': String(),
    'bed_count': Integer(),
    'guest_count': Integer(),
    'property_type': String(),
    'room_type': String(),
    'price': Integer(),
    'rating' : Integer(),
}

# Dump DF
df.to_sql('properties_df', con=Engine, if_exists='replace', dtype = dtype_mapping, index_label='id')

# Copy the DF table to our sql table
sql = ('insert into properties '
       'select id, lga, property_type, room_type, guest_count, bed_count, rating, price '
       'from properties_df')
Engine.execute(sql)

# Drop the df table
Engine.execute('drop table properties_df')

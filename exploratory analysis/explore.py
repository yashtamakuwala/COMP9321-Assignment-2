import os
import pandas as pd
import copy
import math, numpy
os.chdir("..")
root = os.path.abspath(os.curdir)
path_of_data = os.path.join(root, 'data/listings.csv')
df = pd.read_csv(path_of_data)
'''
Convert string to float 
'''
def convert_to_float(i):
    # it changes to float only when values are str
    if (isinstance(i,str)):
        return float (i.replace(',','').replace('$',''))
    return i

def convert_to_int(i):
    i = int(i)
    return i

required_columns = ["latitude","longitude", "bathrooms","bedrooms",
            "square_feet","minimum_nights","maximum_nights","price","weekly_price","monthly_price"]
# the values of these columns would be converted to int
integer_columns = ["bathrooms","bedrooms","minimum_nights","maximum_nights"]
# few more columns
additional_columns = ["accommodates","property_type","bed_type"]

for i in integer_columns:
    df[i] = df[i].fillna(int(-1))
df3 = df[required_columns]

# copy df3 to df3 
df4 = df3.copy()

for k in required_columns:
    if (k in integer_columns):
        df4[k] = df3[k].apply(convert_to_int)
    else:
        df4[k] = df3[k].apply(convert_to_float)


for i in additional_columns:
    df4[additional_columns] = df[additional_columns]
# print only 10 rows
print(df4.iloc[:10])
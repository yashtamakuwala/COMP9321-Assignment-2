
import os
import pandas as pd
import copy
import math
import numpy as np
from sklearn.metrics import confusion_matrix 
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier 
from sklearn.metrics import accuracy_score 
from sklearn.metrics import classification_report 
from sklearn.preprocessing import LabelEncoder
import re
import pickle
from sklearn.neighbors import KNeighborsClassifier
from sklearn.utils import shuffle
from sklearn.metrics import precision_score, accuracy_score, recall_score


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
def convert_to_str(i):
    return str(i)

required_columns = ["latitude","longitude", "bathrooms","bedrooms",
            "square_feet","minimum_nights","maximum_nights","price","weekly_price","monthly_price","beds"]
# the values of these columns would be converted to int
integer_columns = ["bathrooms","bedrooms","minimum_nights","maximum_nights","beds"]
# few more columns thar are strings
additional_columns = ["accommodates","property_type","bed_type","zipcode","room_type"]

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
        
#adding additional columns in df4
for i in additional_columns:
    df4[additional_columns] = df[additional_columns]


#the 5 columns that required for the ML algorithm 
df4 = df4[["property_type","accommodates","beds","room_type","zipcode","price"]]
df4 = df4.drop(df4[(df4.price > 10000.00)].index)
'''
The bins are decided here
The labels are one less than the size of bins
'''
bins = [-0.1,10,70,200,500,2000,5000, 10000]
labels = [i for i in range(1,len(bins))]

#add another column price_bin
df4['price_bin'] = pd.cut(df4['price'], bins=bins, labels=labels)

#The main df on which we creaTE OUR ML MODEL
'''
THe label encoder which does the preprocessing
where categorical data is converted to numerical.
'''
le_property_type = LabelEncoder()

le_room_type = LabelEncoder()
le_zipcode = LabelEncoder()

'''
the 3 columns are updated with the preprocessed values
'''
df4['property_type'] = le_property_type.fit_transform(df4['property_type'])
df4['room_type'] = le_room_type.fit_transform(df4['room_type'])

df4['zipcode'] = df4['zipcode'].apply(convert_to_str)
df4['zipcode'] = le_zipcode.fit_transform(df4['zipcode'])
print(list(le_property_type.classes_))
#X axis would have columns "property_type","accommodates","beds","room_type","zipcode"
Xaxis = df4.values[:, [0,1,2,3,4]] 
# Y axis would have price bins
Yaxis = df4.values[:,6]
Xaxis =Xaxis.astype('int') 
Yaxis = Yaxis.astype('int')


X_train, X_test, y_train, y_test = train_test_split(  
        Xaxis, Yaxis, test_size = 0.33, random_state = 100)
# predict the test set
#Gini impurity an entropy are what are called selection criterion for decision trees. 

# the probability of a random sample being classified incorrectly.
gini = DecisionTreeClassifier(criterion = "gini", 
        random_state = 100,max_depth=3, min_samples_leaf=5) 
gini.fit(X_train, y_train)
#-------------------------------------------------------------
#measurement of information
entropy = DecisionTreeClassifier( 
        criterion = "entropy", random_state = 100, 
        max_depth = 3, min_samples_leaf = 5) 
entropy.fit(X_train, y_train)
#-------------------------------------------------------------
y_pred = gini.predict(X_test)
entropy_pred = entropy.predict(X_test)
# To store the Machine learning model- PICKLE is used
os.chdir("exploratory analysis/")
filename = 'price_prediction_model.sav'
if ((accuracy_score(y_test,y_pred)*100) >= (accuracy_score(y_test,entropy_pred)*100) ):
    with open(filename, 'wb') as file:  
        pickle.dump(gini, file)
else:
    with open(filename, 'wb') as file:  
        pickle.dump(entropy, file)



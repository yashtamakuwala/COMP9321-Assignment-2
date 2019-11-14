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

def lower_and_remove_special_char(df,col):
    #df[col] = df[col].apply(lambda x: x.split()[0].strip().lower() if x else None)
    df[col] = df[col].apply(lambda x: x.replace(',',''))
    df[col] = df[col].str.replace(r"[^a-zA-Z\d\_]+", "")    
    df[col] = df[col].str.replace(r"[^a-zA-Z\d\_]+", "")
    return df

def convert_to_type_and_clean(df, df3, df4, integer_columns, required_columns, additional_columns):
    for k in required_columns:
        if (k in integer_columns):
            df4[k] = df3[k].apply(convert_to_int)
        else:
            df4[k] = df3[k].apply(convert_to_float)
            
    #adding additional columns in df4
    df4[additional_columns] = df[additional_columns]
    df4['city'] = df4['city'].apply(convert_to_str)
    #print(sorted(df4['city'].unique()))
    #the 5 columns that required for the ML algorithm         
    df4 = df4[["property_type","accommodates","beds","room_type","zipcode","price","city"]]
    df4 = df4.drop(df4[(df4.price > 10000.00)].index)
    #df4 = lower_and_remove_special_char(df4,"city")

    df4 = df4[df4.city != '']
    return df4


class Trainer:
    def train(self):
        os.chdir("..")
        os.chdir("..")
        root = os.path.abspath(os.curdir)
        path_of_data = os.path.join(root, 'data/listings.csv')
        path_of_data2 = os.path.join(root, 'data/RCI_OffenceByMonth2.csv')
        df = pd.read_csv(path_of_data)
        dfc = pd.read_csv(path_of_data2)
        dfc['LGA']
        
        required_columns = ["latitude","longitude", "bathrooms","bedrooms",
                    "square_feet","minimum_nights","maximum_nights","price","weekly_price","monthly_price","beds"]
        # the values of these columns would be converted to int
        integer_columns = ["bathrooms","bedrooms","minimum_nights","maximum_nights","beds"]
        # few more columns thar are strings
        additional_columns = ["accommodates","property_type","bed_type","zipcode","room_type","city"]
        for i in integer_columns:
            df[i] = df[i].fillna(int(-1))
        df3 = df[required_columns]
        # copy df3 to df3 
        df4 = df3.copy()
        df4 = convert_to_type_and_clean(df, df3, df4, integer_columns,
                            required_columns, additional_columns)
        #a = df4["city"].unique()
        #print(sorted(a)
        #dfc = lower_and_remove_special_char(dfc,"LGA")
        dfc['city'] = dfc['LGA']
        range_of_col = [i for i in range(4,220)]
        #df4 = df4.merge(dfc,on="city", how = "left")
        #dfc = dfc[pd.notnull(dfc['LGA'])]
        print(df4['city'].value_counts().to_dict())
        #print(df4['city'].unique())
        #print(dfc['LGA'].isna().sum())

        print(dfc.columns)
        '''
        The bins are decided here
        The labels are one less than the size of bins
        '''
        bins = [-0.1,10,70,200,500,2000,5000, 10000]
        labels = [i for i in range(1,len(bins))]

        #add another column price_bin
        df4['price_bin'] = pd.cut(df4['price'], bins=bins, labels=labels)

        #The main df on which we creaTE OUR ML MODEL
       
        #THe label encoder which does the preprocessing
        #where categorical data is converted to numerical.

        le_property_type = LabelEncoder()
        le_room_type = LabelEncoder()
        le_zipcode = LabelEncoder()
     
        #the 3 columns are updated with the preprocessed values

        #print(df4['property_type'].iloc[:5])
        '''
        df4['property_type'] = le_property_type.fit_transform(df4['property_type'])
        df4['room_type'] = le_room_type.fit_transform(df4['room_type'])
        df4['zipcode'] = df4['zipcode'].apply(convert_to_str)
        df4['zipcode'] = le_zipcode.fit_transform(df4['zipcode'])
        #print(le_zipcode.classes_)
        np.save('classes.npy', le_property_type.classes_)
        #print(df4['property_type'].iloc[:5])

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
        os.chdir("tahelka/ml")
        filename = 'price_prediction_model.sav'
        file_for_zipcode = open('zipcode_encoder.pkl', 'wb')
        pickle.dump(le_zipcode,file_for_zipcode)
        #consider the model with higher accuracy
        if ((accuracy_score(y_test,y_pred)*100) >= (accuracy_score(y_test,entropy_pred)*100) ):
            with open(filename, 'wb') as file:  
                pickle.dump(gini, file)
        else:
            with open(filename, 'wb') as file:  
                pickle.dump(entropy, file)
        '''

train_model = Trainer()
train_model.train()

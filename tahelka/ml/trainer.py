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
from alchemy import Engine
from sklearn.utils import shuffle
from sklearn.metrics import precision_score, accuracy_score, recall_score

class Trainer:
    '''PRICE_BUCKETS = [-1, 40, 50, 60, 70, 80, 90, 100, 115, 125, 140, 150, 175, 200, 210,
                     250, 300, 400, 600, 100_000]
    '''
    PRICE_BUCKETS = [-1, 40, 60, 80, 100, 125, 150, 200, 250, 300, 500, 99_999]
    CRIME_BUCKETS = [-1, 250, 500, 1000, 1500, 100_000]
    UNEMP_BUCKETS = [-1, 2, 4, 6, 8, 100_000]

    def train(self):
        df = self.prepare_ml_df()
        le_property_type = LabelEncoder()
        le_room_type = LabelEncoder()
        df['property_type'] = le_property_type.fit_transform(df['property_type'])
        df['room_type'] = le_room_type.fit_transform(df['room_type'])
        #print(le_property_type.classes_)
        #np.save('classes.npy', le_property_type.classes_)
        Xaxis = df.values[:, [0,1,2,3,5,6]]
        #print(df)
        # Y axis would have price bins
        Yaxis = df.values[:,4]
        Xaxis =Xaxis.astype('int')
        Yaxis = Yaxis.astype('int')
        X_train, X_test, y_train, y_test = (
            train_test_split(Xaxis, Yaxis, test_size=0.33, random_state=100
        )

        #Gini impurity an entropy are what are called selection criterion for decision trees.

        ### GINI ###
        gini = DecisionTreeClassifier(criterion = "gini",
                random_state = 100,max_depth=3, min_samples_leaf=5)
        gini.fit(X_train, y_train)
        ### ENTROPY ###
        entropy = DecisionTreeClassifier(
                criterion = "entropy", random_state = 100,
                max_depth = 3, min_samples_leaf = 5)
        entropy.fit(X_train, y_train)
        ### MODEL CREATION  ####
        y_pred = gini.predict(X_test)
        entropy_pred = entropy.predict(X_test)

        errors = 0
        count = 0

        for index, pred in enumerate(y_pred):
            #print(X_test[index], y_test[index], pred)
            errors += abs(pred - y_test[index])
            count += 1

        print(f'mean error: {errors / len(y_pred)}')


        filename = 'price_prediction_model.sav'

        #consider the model with higher accuracy
        print(accuracy_score(y_test,y_pred)*100)
        print(accuracy_score(y_test,entropy_pred)*100)

        if ((accuracy_score(y_test,y_pred)*100) >= (accuracy_score(y_test,entropy_pred)*100) ):
            with open(filename, 'wb') as file:
                pickle.dump(gini, file)
        else:
            with open(filename, 'wb') as file:
                pickle.dump(entropy, file)



        '''
        os.chdir("..")
        os.chdir("..")
        root = os.path.abspath(os.curdir)
        path_of_data = os.path.join(root, 'data/listings.csv')
        path_of_data2 = os.path.join(root, 'data/RCI_OffenceByMonth2.csv')
        df = pd.read_csv(path_of_data)
        dfc = pd.read_csv(path_of_data2)

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

        The bins are decided here
        The labels are one less than the size of bins

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
    def prepare_ml_df(self):
        # Load dataframe
        df = pd.read_sql_table('properties', con=Engine)

        # Remove unneeded columns
        df = df.drop(['id','rating'], axis=1)

        # Put price into buckets
        df['price_range'] = pd.cut(df['price'], bins=Trainer.PRICE_BUCKETS,
                                   labels=range(1, len(Trainer.PRICE_BUCKETS)))

        print(df['price_range'].value_counts())

        # Remove price column
        df = df.drop(['price'], axis=1)

        # Get crime & unemp dfs
        dfc = self.prepare_crime_df()
        dfu = self.prepare_unemp_df()

        # Merge DF with DFC
        df = df.merge(dfc, left_on = "lga", right_on = "LGA" )
        df = df.drop(['LGA'], axis = 1)

        # Merge DF with DFU
        df = df.merge(dfu, left_on = "lga", right_on = "LGA" )
        df = df.drop(['LGA'], axis = 1)

        # Drop lga
        df = df.drop(['lga'], axis=1)
        return df

    def prepare_crime_df(self):
        # Load DFC
        root = os.path.abspath(os.curdir)
        path_of_data = os.path.join(root, 'data/crime_clean.csv')
        dfc = pd.read_csv(path_of_data)

        # Get monthly mean of crime count
        month_columns = dfc.columns[1:]
        dfc['mean_crime_count'] = dfc[month_columns].mean(axis='columns')

        # Drop month columns
        dfc = dfc.drop(month_columns, axis=1)

        # Group by LGA
        dfc = dfc.groupby(['LGA']).sum().reset_index()

        # Mean crime count to crime levels
        dfc['crime_level'] = pd.cut(dfc['mean_crime_count'], bins=Trainer.CRIME_BUCKETS,
                                    labels=range(1, len(Trainer.CRIME_BUCKETS)))
        dfc = dfc.drop(['mean_crime_count'], axis=1)

        return dfc

    def prepare_unemp_df(self):
        # Load DFU
        root = os.path.abspath(os.curdir)
        path_of_data = os.path.join(root, 'data/unemployment_clean.csv')
        dfu = pd.read_csv(path_of_data)

        # Get monthly mean of unemp count
        month_columns = dfu.columns[1:]
        dfu['mean_unemp_count'] = dfu[month_columns].mean(axis='columns')

        # Drop month columns
        dfu = dfu.drop(month_columns, axis=1)

        # Mean crime count to crime levels
        dfu['unemp_level'] = pd.cut(dfu['mean_unemp_count'], bins=Trainer.UNEMP_BUCKETS,
                            labels=range(1, len(Trainer.UNEMP_BUCKETS)))
        dfu = dfu.drop(['mean_unemp_count'], axis=1)

        return dfu

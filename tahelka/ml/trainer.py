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
    PRICE_BUCKETS = [-1, 40, 60, 80, 100, 125, 150, 200, 250, 300, 500, 99_999]
    CRIME_BUCKETS = [-1, 250, 500, 1000, 1500, 100_000]
    UNEMP_BUCKETS = [-1, 2, 4, 6, 8, 100_000]

    def train(self):
        df = self.prepare_ml_df()   

        # Encode the categorical attributes
        le_property_type = LabelEncoder()
        le_room_type = LabelEncoder()
        df['property_type'] = le_property_type.fit_transform(df['property_type'])
        df['room_type'] = le_room_type.fit_transform(df['room_type'])

        # Get X & Y
        Xaxis = df.values[:, [0,1,2,3,5,6]].astype('int')
        Yaxis = df.values[:,4].astype('int')

        # Create the model
        gini = DecisionTreeClassifier(criterion="gini",
                                      random_state = 100, max_depth=3, min_samples_leaf=5)
        gini.fit(Xaxis, Yaxis)

        # Save gini model using pickle
        with open('ml_models/model.sav', 'wb') as file:
            pickle.dump(gini, file)

        file_for_prop = open('ml_models/property_type_encoding.sav', 'wb')
        file_for_room = open('ml_models/room_type_encoding.sav', 'wb')
        pickle.dump(le_property_type,file_for_prop)
        pickle.dump(le_room_type,file_for_room)

    def prepare_ml_df(self):
        # Load dataframe
        df = pd.read_sql_table('properties', con=Engine)
        # Remove unneeded columns
        df = df.drop(['id','rating'], axis=1)

        # Put price into buckets
        df['price_range'] = pd.cut(df['price'], bins=Trainer.PRICE_BUCKETS,
                                   labels=range(1, len(Trainer.PRICE_BUCKETS)))
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

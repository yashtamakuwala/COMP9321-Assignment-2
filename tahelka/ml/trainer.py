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
from tahelka.ml.crime_level_preparer import CrimeDataframePreparer
from tahelka.ml.unemp_level_preparer import UnempDataframePreparer

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
        dfc = CrimeDataframePreparer.prepare()
        dfu = UnempDataframePreparer.prepare()

        # Merge DF with DFC
        df = df.merge(dfc, left_on = "lga", right_on = "LGA" )
        df = df.drop(['LGA'], axis = 1)

        # Merge DF with DFU
        df = df.merge(dfu, left_on = "lga", right_on = "LGA" )
        df = df.drop(['LGA'], axis = 1)

        # Drop lga
        df = df.drop(['lga'], axis=1)

        return df

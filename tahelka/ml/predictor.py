import os
import warnings
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from tahelka.ml.crime_level_preparer import CrimeDataframePreparer
from tahelka.ml.unemp_level_preparer import UnempDataframePreparer
from werkzeug.exceptions import BadRequest

warnings.filterwarnings("ignore", category=DeprecationWarning)

class Predictor:
    PRICE_BUCKETS = [-1, 40, 60, 80, 100, 125, 150, 200, 250, 300, 500, 99_999]
    def __init__(self,lga, property_type, room_type, guest_count,
                 bed_count):
        self.lga = lga
        self.property_type = property_type
        self.room_type = room_type
        self.guest_count = guest_count
        self.bed_count = bed_count

    def predict(self):
        property_encoding_file = open('ml_models/property_type_encoding.sav', 'rb')
        room_type_encoding_file= open('ml_models/room_type_encoding.sav', 'rb')
        property_type_encoder = pickle.load(property_encoding_file)
        room_type_encoder = pickle.load(room_type_encoding_file)

        filename = 'ml_models/model.sav'
        with open(filename, 'rb') as file:
            loaded_model = pickle.load(file)

        try:
            self.property_type = property_type_encoder.transform([self.property_type])[0]
            self.room_type = room_type_encoder.transform([self.room_type])[0]
        except(ValueError): # If unexpected property type and room type input
            raise BadRequest

        dfc = CrimeDataframePreparer.prepare()
        crime_levels = dfc.loc[dfc['LGA'] == self.lga, 'crime_level']
        if len(crime_levels) == 0: # If no such LGA, raise error
            raise BadRequest
        crime_level = crime_levels.iloc[0]

        dfu = UnempDataframePreparer.prepare()
        unemp_levels = dfu.loc[dfu['LGA'] == self.lga, 'unemp_level']
        if len(unemp_levels) == 0: # If no such LGA, raise error
            raise BadRequest
        unemp_level = unemp_levels.iloc[0]

        X_test = [[self.property_type, self.room_type, self.guest_count, self.bed_count, crime_level, unemp_level]]
        predicted_result = loaded_model.predict(X_test)

        return self.find_range(predicted_result[0], Predictor.PRICE_BUCKETS, 0, 0)

    def find_range(self, result, buckets, lower ,upper):
        bucket_len = len(buckets)
        if result == 1:
            return {'upper': buckets[1]}
        elif result == bucket_len - 1:
            return {'lower' : buckets[bucket_len - 2]}
        return {'lower' : buckets[result - 1], 'upper': buckets[result]}

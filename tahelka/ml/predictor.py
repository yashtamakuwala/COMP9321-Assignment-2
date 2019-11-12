import os
import warnings
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder
warnings.filterwarnings("ignore", category=DeprecationWarning) 
filename = 'price_prediction_model.sav'

#X axis would have columns "property_type","accommodates","beds","room_type","zipcode"
# need to refer to the values of label encoders for X_test values
le_property_type = LabelEncoder()
le_room_type = LabelEncoder()
le_zipcode = LabelEncoder()

# The encoding for property_type
le_property_type.fit_transform(['Aparthotel', 'Apartment', 'Barn', 'Bed and breakfast', 'Boat', 
'Boutique hotel', 'Bungalow', 'Cabin', 'Camper/RV', 'Campsite', 'Casa particular (Cuba)', 
'Castle', 'Cave', 'Chalet', 'Condominium', 'Cottage', 'Dome house', 'Earth house', 'Farm stay', 
'Guest suite', 'Guesthouse', 'Heritage hotel (India)', 'Hostel', 'Hotel', 'House', 
'Island', 'Loft', 'Minsu (Taiwan)', 'Other', 'Resort', 'Serviced apartment', 
'Tent', 'Tiny house', 'Tipi', 'Townhouse', 'Train', 'Treehouse', 'Villa', 'Yurt'])
#encoding for room_type
le_room_type.fit_transform(['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'])

#stored model for zip code
zip_code_file = open('zipcode_encoder.pkl', 'rb')
le_zipcode = pickle.load(zip_code_file)
zip_code_file.close()


print(le_zipcode.classes_)
class Predictor:
    def __init__(self, zip_code, property_type, room_type, guest_count,
                 bed_count):
        self.zip_code = zip_code
        self.property_type = property_type
        self.room_type = room_type
        self.guest_count = guest_count
        self.bed_count = bed_count

    def predict(self):

        pass



with open(filename, 'rb') as file:  
    loaded_model = pickle.load(file)


'''
 Property-Type - 


'''
''' Room type - 
'''
X_test = [[3,1,2,4,8]]
result = loaded_model.predict(X_test)
print(result)
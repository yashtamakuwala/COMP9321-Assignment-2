import os
import warnings
import pickle
warnings.filterwarnings("ignore", category=DeprecationWarning) 
filename = 'price_prediction_model.sav'
with open(filename, 'rb') as file:  
    loaded_model = pickle.load(file)
#X axis would have columns "property_type","accommodates","beds","room_type","zipcode"
# need to refer to the values of label encoders for X_test values

'''
 Property-Type - 
['Aparthotel', 'Apartment', 'Barn', 'Bed and breakfast', 'Boat', 
'Boutique hotel', 'Bungalow', 'Cabin', 'Camper/RV', 'Campsite', 'Casa particular (Cuba)', 
'Castle', 'Cave', 'Chalet', 'Condominium', 'Cottage', 'Dome house', 'Earth house', 'Farm stay', 
'Guest suite', 'Guesthouse', 'Heritage hotel (India)', 'Hostel', 'Hotel', 'House', 
'Island', 'Loft', 'Minsu (Taiwan)', 'Other', 'Resort', 'Serviced apartment', 
'Tent', 'Tiny house', 'Tipi', 'Townhouse', 'Train', 'Treehouse', 'Villa', 'Yurt']

'''
''' Room type - 
['Entire home/apt', 'Hotel room', 'Private room', 'Shared room']'''
X_test = [[3,1,2,4,8]]
result = loaded_model.predict(X_test)
print(result)
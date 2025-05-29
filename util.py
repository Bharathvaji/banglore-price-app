import json
import pickle
import numpy as np

__locations = None
__data_columns = None
__model = None

def load_saved_artifacts():
    global __data_columns
    global __locations
    global __model

    with open("artifacts/columns.json", "r") as f:
        __data_columns = [col.lower() for col in json.load(f)['data_columns']]
        __locations = __data_columns[3:]  # assuming first 3 are numeric

    with open("artifacts/banglore_home_prices_model.pickle", "rb") as f:
        __model = pickle.load(f)

def predict_price(location, sqft, bath, bhk):
    location = location.lower()
    try:
        loc_index = __locations.index(location)
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk

    if loc_index >= 0:
        x[loc_index + 3] = 1  # offset by 3

    return round(__model.predict([x])[0], 2)

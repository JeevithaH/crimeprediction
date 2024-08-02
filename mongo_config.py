import pandas as pd
from pymongo import MongoClient


def base_config():
    data = pd.read_csv(r"data/crime_2023.csv")
    data = data[(data['DISTRICT'] != 'TOTAL') & (data['DISTRICT'] != 'ZZ TOTAL')]

    client = MongoClient('mongodb://localhost:27017')
    db = client['Crime_Precision']
    users_collection = db['User_Data']
    return data, users_collection

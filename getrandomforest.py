import pickle

# Load the model from the file
with open('random_forest_model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

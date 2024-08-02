import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle

# Load the dataset
data = pd.read_csv(r"data/crime_2023.csv")

data = data[(data['DISTRICT'] != 'TOTAL') & (data['DISTRICT'] != 'ZZ TOTAL')]

# Split data into features and target variable
X = data.drop(columns=["STATE/UT", "DISTRICT", "YEAR", "TOTAL IPC CRIMES"])  # Features
y = data["TOTAL IPC CRIMES"]  # Target variable

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model training
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model to a file
with open('random_forest_model.pkl', 'wb') as file:
    pickle.dump(model, file)





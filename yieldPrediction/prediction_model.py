<<<<<<< HEAD
from joblib import load

# Load the trained model
model = load('./ML_Components/DecisionTreeRegressor.joblib')

# DecisionTreeRegressor
# LinearRegression
# MLPRegressor
# SVR

# Load the scaler
scaler = load('./ML_Components/scaler.joblib')


def scale_data(new_data, scaler):
    # Apply the scaling transformation to the new data
    scaled_data = scaler.transform(new_data)
    return scaled_data

# Define a function to make predictions on scaled new data
def make_predictions(scaled_data, model):
    # Make predictions using the loaded model
    predictions = model.predict(scaled_data)
=======
from joblib import load

# Load the trained model
model = load('./savedModels/LinearRegression.joblib')

# Load the scaler
scaler = load('./savedModels/scaler.joblib')


def scale_data(new_data, scaler):
    # Apply the scaling transformation to the new data
    scaled_data = scaler.transform(new_data)
    return scaled_data

# Define a function to make predictions on scaled new data
def make_predictions(scaled_data, model):
    # Make predictions using the loaded model
    predictions = model.predict(scaled_data)
>>>>>>> 7ef29c090b6300e9d7ec70a747fd81796baea790
    return predictions
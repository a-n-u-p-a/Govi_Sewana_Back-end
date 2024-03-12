from joblib import load

# Load the trained model
model = load('./savedModels/DecisionTreeRegressor.joblib')
# LinearRegression
# DecisionTreeRegressor
# MLPRegressor

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
    return predictions
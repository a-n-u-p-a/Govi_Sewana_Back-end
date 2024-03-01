import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

from joblib import load
import pandas as pd

# Load the fitted scaler
scaler = load('scaler.joblib')

# Load the trained model
regr = load('DecisionTreeRegressor.joblib')

# Define a function to scale new data using the loaded scaler
def scale_data(new_data, scaler):
    # Apply the scaling transformation to the new data
    scaled_data = scaler.transform(new_data)
    return scaled_data

# Define a function to make predictions on scaled new data
def make_predictions(scaled_data, model):
    # Make predictions using the loaded model
    predictions = model.predict(scaled_data)
    return predictions


# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 6.9708,
	"longitude": 80.7829,
	"daily": ["apparent_temperature_max", "apparent_temperature_min", "daylight_duration", "sunshine_duration", "rain_sum", "precipitation_hours", "shortwave_radiation_sum", "et0_fao_evapotranspiration"],
	"forecast_days": 7
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_apparent_temperature_max = daily.Variables(0).ValuesAsNumpy()
daily_apparent_temperature_min = daily.Variables(1).ValuesAsNumpy()
daily_daylight_duration = daily.Variables(2).ValuesAsNumpy()
daily_sunshine_duration = daily.Variables(3).ValuesAsNumpy()
daily_rain_sum = daily.Variables(4).ValuesAsNumpy()
daily_precipitation_hours = daily.Variables(5).ValuesAsNumpy()
daily_shortwave_radiation_sum = daily.Variables(6).ValuesAsNumpy()
daily_et0_fao_evapotranspiration = daily.Variables(7).ValuesAsNumpy()

daily_data = {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}

daily_data["Temperature"] = (daily_apparent_temperature_max + daily_apparent_temperature_min)/2
daily_data["daylight(s)"] = daily_daylight_duration
daily_data["sunshine(s)"] = daily_sunshine_duration
daily_data["rain_sum (mm)"] = daily_rain_sum
daily_data["precipitation_hours (h)"] = daily_precipitation_hours
daily_data["shortwave_radiation_sum (MJ/mÂ²)"] = daily_shortwave_radiation_sum
daily_data["et0_fao_evapotranspiration (mm)"] = daily_et0_fao_evapotranspiration

daily_dataframe = pd.DataFrame(data = daily_data)

#taking extent as an input
extent = float(input("Enter the extent: ")) 

#taking avg and sum values
average_temperature = daily_dataframe["Temperature"].mean()
daylight_sum = daily_dataframe["daylight(s)"].sum()
sunshine_sum = daily_dataframe["sunshine(s)"].sum()
rain_sum = daily_dataframe["rain_sum (mm)"].sum()
average_precipitation = daily_dataframe["precipitation_hours (h)"].mean()
average_radiation = daily_dataframe["shortwave_radiation_sum (MJ/mÂ²)"].mean()
average_evapotranspiration = daily_dataframe["et0_fao_evapotranspiration (mm)"].mean()

#pd dataframe that consists of ml features
average_data = pd.DataFrame ({
    'recorded extent': [extent],
    'Temperature': [average_temperature],
    'daylight(s)': [daylight_sum],
    'sunshine(s)': [sunshine_sum],
    'rain_sum (mm)': [rain_sum],
    'precipitation_hours (h)': [average_precipitation],
    'shortwave_radiation_sum (MJ/mÂ²)': [average_radiation],
    'et0_fao_evapotranspiration (mm)': [average_evapotranspiration]
})


print(average_data)

#passing features to scale
scaled_new_data = scale_data(average_data, scaler)

# Make predictions on the scaled new data
new_predictions = make_predictions(scaled_new_data, regr)

# Print the predictions
print(new_predictions)

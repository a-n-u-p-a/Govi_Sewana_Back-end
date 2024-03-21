from django.shortcuts import render
<<<<<<< HEAD
from .models import user_collection, yield_collection, excess_collection
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

import pandas as pd
import datetime

# Import python files
import yieldPrediction.weatherAPI as wapi
import yieldPrediction.prediction_model as pm

@api_view(['POST'])
# Function to make predictions on new data
def predictor(request):
    if request.method == 'POST':
        try:
            # Assuming you're expecting JSON data
            cultivationData = request.data # Use request.data to get the JSON data 
            crop_type = cultivationData.get("Crop_Type")
            date = cultivationData.get("Date_of_Planting")
            #recorded_extent = int(cultivationData.get("crop_Extent(Acres)"))
            recorded_extent = cultivationData.get("crop_Extent(Acres)")

            # Assuming you have a date variable 'date' in the format 'yyyy-mm-dd'
            start_date = datetime.datetime.strptime(date, "%Y-%m-%d")

            # Add 90 days to the date
            upadate_date = start_date + datetime.timedelta(days=90)
            harvest_date = upadate_date.strftime("%Y-%m-%d")

            #Get the week number using isocalender()
            week_number = upadate_date.isocalendar().week

            weather_data = wapi.processWeatherData()

            average_temperature = weather_data[0]
            daylight_sum = weather_data[1]
            sunshine_sum = weather_data[2]
            rain_sum = weather_data[3]
            average_precipitation = weather_data[4]
            average_radiation = weather_data[5]
            average_evapotranspiration = weather_data[6]

            #pd dataframe that consists of ml features
            average_data = pd.DataFrame ({
                'recorded extent': [recorded_extent],
                'Temperature': [average_temperature],
                'daylight(s)': [daylight_sum],
                'sunshine(s)': [sunshine_sum],
                'rain_sum (mm)': [rain_sum],
                'precipitation_hours (h)': [average_precipitation],
                'shortwave_radiation_sum (MJ/mÂ²)': [average_radiation],
                'et0_fao_evapotranspiration (mm)': [average_evapotranspiration]
            })

            scaled_new_data = pm.scale_data(average_data, pm.scaler)

            # Make predictions on the scaled new data
            new_predictions = pm.make_predictions(scaled_new_data, pm.model)

            # Add and update data to Json object
            cultivationData["crop_Extent(Acres)"] = float(recorded_extent)
            cultivationData["Date_of_Harvest"] = harvest_date
            cultivationData["Harvest_Week_No."] = week_number
            cultivationData["Predicted_Yield(T)"] = new_predictions[0]
            

            # Insert data in to Crop_Yield collection
            yield_collection.insert_one(cultivationData)
        
            # Sending the predicted yield to the front end
            return Response({"predictedYield": new_predictions[0], "harvestDate": harvest_date, "weekNumber": week_number})
        
        except Exception as e:
            return HttpResponse("error: "+str(e))
        
        
=======
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

from joblib import load
import pandas as pd

# Load the scaler
scaler = load('scaler.joblib')

# Load the trained model
model = load('./savedModels/MLPRegressor.joblib')

def scale_data(new_data, scaler):
    # Apply the scaling transformation to the new data
    scaled_data = scaler.transform(new_data)
    return scaled_data

# Define a function to make predictions on scaled new data
def make_predictions(scaled_data, model):
    # Make predictions using the loaded model
    predictions = model.predict(scaled_data)
    return predictions


# Function to make predictions on new data
def predictor(request):
    if request.method == 'POST':
        crop_type = request.POST['crop_type']
        date = request.POST['date']
        recorded_extent = request.POST['crop_extent']

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
            'recorded extent': [recorded_extent],
            'Temperature': [average_temperature],
            'daylight(s)': [daylight_sum],
            'sunshine(s)': [sunshine_sum],
            'rain_sum (mm)': [rain_sum],
            'precipitation_hours (h)': [average_precipitation],
            'shortwave_radiation_sum (MJ/mÂ²)': [average_radiation],
            'et0_fao_evapotranspiration (mm)': [average_evapotranspiration]
        })
        # temperature = request.POST['temperature']
        # daylight = request.POST['daylight']
        # sunshine = request.POST['sunshine']
        # rain_sum = request.POST['rain_sum']
        # precipitation_hours = request.POST['precipitation_hours']
        # shortwave_radiation_sum = request.POST['shortwave_radiation_sum']
        # evapotranspiration = request.POST['evapotranspiration']

        # Convert to Numeric Data Type
        # recorded_extent_numeric = float(recorded_extent)
        # temperature_numeric = float(average_temperature)
        # daylight_numeric = float(daylight_sum)
        # sunshine_numeric = float(sunshine_sum)
        # rain_sum_numeric = float(rain_sum)
        # precipitation_hours_numeric = float(average_precipitation)
        # shortwave_radiation_sum_numeric = float(average_radiation)
        # evapotranspiration_numeric = float(average_evapotranspiration)

        scaled_new_data = scale_data(average_data, scaler)

        # Make predictions on the scaled new data
        new_predictions = make_predictions(scaled_new_data, model)
    
        # y_pred = model.predict([[recorded_extent_numeric, temperature_numeric, daylight_numeric, sunshine_numeric, rain_sum_numeric, precipitation_hours_numeric, shortwave_radiation_sum_numeric, evapotranspiration_numeric]])
        
        return render(request, 'main.html', {'result' : new_predictions})

    return render(request, 'main.html')
    
>>>>>>> 385e3dce0edacb6e9477ceb06e128733ae21d8d9

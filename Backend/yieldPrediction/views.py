from django.shortcuts import render
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
        
        

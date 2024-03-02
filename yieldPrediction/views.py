from django.shortcuts import render

import pandas as pd

# Import python files
import yieldPrediction.weatherAPI as wapi
import yieldPrediction.prediction_model as pm

# Function to make predictions on new data
def predictor(request):
    if request.method == 'POST':
        crop_type = request.POST['crop_type']
        date = request.POST['date']
        recorded_extent = request.POST['crop_extent']

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
        
        return render(request, 'main.html', {'result' : new_predictions})

    return render(request, 'main.html')
    
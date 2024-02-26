from django.shortcuts import render

from joblib import load

# Load the trained model
model = load('./savedModels/MLPRegressor.joblib')

# Function to make predictions on new data
def predictor(request):
    if request.method == 'POST':
        crop_type = request.POST['crop_type']
        date = request.POST['date']
        recorded_extent = request.POST['crop_extent']
        temperature = request.POST['temperature']
        daylight = request.POST['daylight']
        sunshine = request.POST['sunshine']
        rain_sum = request.POST['rain_sum']
        precipitation_hours = request.POST['precipitation_hours']
        shortwave_radiation_sum = request.POST['shortwave_radiation_sum']
        evapotranspiration = request.POST['evapotranspiration']

        # Convert to Numeric Data Type
        recorded_extent_numeric = float(recorded_extent)
        temperature_numeric = float(temperature)
        daylight_numeric = float(daylight)
        sunshine_numeric = float(sunshine)
        rain_sum_numeric = float(rain_sum)
        precipitation_hours_numeric = float(precipitation_hours)
        shortwave_radiation_sum_numeric = float(shortwave_radiation_sum)
        evapotranspiration_numeric = float(evapotranspiration)
    
        y_pred = model.predict([[recorded_extent_numeric, temperature_numeric, daylight_numeric, sunshine_numeric, rain_sum_numeric, precipitation_hours_numeric, shortwave_radiation_sum_numeric, evapotranspiration_numeric]])
        
        return render(request, 'main.html', {'result' : y_pred})

    return render(request, 'main.html')
    
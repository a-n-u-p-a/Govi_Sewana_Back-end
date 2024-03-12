from django.shortcuts import render
from django.shortcuts import render, redirect
from django.conf import settings
from twilio.rest import Client


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


client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def send_otp(request):
    if request.method == "POST":
        phone_number = request.POST.get('phone_number')
        verification = client.verify.v2.services(settings.TWILIO_VERIFY_SERVICE_ID) \
            .verifications \
            .create(to=phone_number, channel='sms')
        print(verification.status)
        request.session['phone_number'] = phone_number  # Store in session
        return redirect('verify_otp') 
    return render(request, 'send_otp.html')

def verify_otp(request):
    if request.method == "POST":
        phone_number = request.session.get('phone_number') 
        otp = request.POST.get('otp')

        verification_check = client.verify.v2.services(settings.TWILIO_VERIFY_SERVICE_ID) \
            .verification_checks \
            .create(to=phone_number, code=otp)

        if verification_check.status == "approved":
            # --- Handle User Login ---
            # Replace this placeholder with your user login logic
            # e.g., request.session['user_id'] = ... 
            return redirect('dashboard') 

        else:
            return render(request, 'verify_otp.html')

    return render(request, 'verify_otp.html') 

def dashboard(request):  # Changed to take 'request'
    return render(request, 'dashboard.html')



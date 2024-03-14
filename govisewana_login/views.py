from django.shortcuts import render, redirect
from django.conf import settings
from twilio.rest import Client
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

from django.shortcuts import render, redirect
from django.conf import settings
from twilio.rest import Client
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

@api_view(['POST'])
def send_otp(request):
  if request.method == "POST":
    mobile_no = request.data
    phone_number = mobile_no.get("Mobile-Number")
    request.session['phone_number'] = phone_number  
    print(phone_number)
    verification = client.verify.v2.services(settings.TWILIO_VERIFY_SERVICE_ID) \
        .verifications \
        .create(to=phone_number, channel='sms')
    if verification.status == 'pending':  
        return Response({"success": True})
    else:
        return Response({"success": False, "error": "OTP sending failed"})

# ... (Rest of your verify_otp and dashboard views) 

@api_view(['POST'])
def verify_otp(request):
    if request.method == "POST":
        phone_number = request.session['phone_number']
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

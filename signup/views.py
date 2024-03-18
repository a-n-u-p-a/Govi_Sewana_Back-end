from django.shortcuts import render

# Create your views here.
from django.conf import settings
from twilio.rest import Client
from rest_framework.decorators import api_view
from rest_framework.response import Response


client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

@api_view(['POST'])
def register_details(request):
  if request.method == "POST":
    registration_data = request.data
    full_name = registration_data.get("Full-Name")
    nic = registration_data.get("NIC")
    phone_number = registration_data.get("Mobile-Number")
    print(full_name)
    print(nic)
    print(phone_number)
    # verification = client.verify.v2.services(settings.TWILIO_VERIFY_SERVICE_ID) \
    #     .verifications \
    #     .create(to=phone_number, channel='sms')
    if settings.TESTING_MODE:
       return Response({"success": True})

# ... (Rest of your verify_otp and dashboard views) 

@api_view(['POST'])
def verify_otp(request):
    if request.method == "POST":
        otp_data = request.data
        phone_number = request.session.get('phone_number')
        print('inside') 
        print(phone_number)
        otp = otp_data.get('Entered-Otp')
        print(otp)
        # verification_check = client.verify.v2.services(settings.TWILIO_VERIFY_SERVICE_ID) \
        #     .verification_checks \
        #     .create(to=phone_number, code=otp)

        # if verification_check.status == "approved":
        if settings.TESTING_MODE:
          return Response({"success": True})
from django.shortcuts import render, redirect
from django.conf import settings
from twilio.rest import Client
from django.http import HttpResponse
from .models import user_collection
import logging
logger = logging.getLogger(__name__) 

from rest_framework.decorators import api_view
from rest_framework.response import Response

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

@api_view(['POST'])
def send_otp(request):
  if request.method == "POST":
    mobile_no = request.data
    phone_number = mobile_no.get("Mobile_Number")
    # check if the user is a registered user
    # Ensure phone_number is a string
    phone_number = str(phone_number)
    print(phone_number)
    # Prepare two versions of the phone number
    if phone_number.startswith('+94') and not phone_number.startswith('+940'):
      phone_number_alt = phone_number.replace('+94', '+940', 1)
    elif phone_number.startswith('+940'):
      phone_number_alt = phone_number.replace('+940', '+94', 1)

    # Update the query to look for either version of the phone number
    existing_number = user_collection.find_one({
        "$or": [
            {"Mobile_Number": phone_number},
            {"Mobile_Number": phone_number_alt}
        ]
    })

    if existing_number:
      print(phone_number_alt)
    else:
      return Response(status=409, data={'message': 'User not found'})

    # verification = client.verify.v2.services(settings.TWILIO_VERIFY_SERVICE_ID) \
    #     .verifications \
    #     .create(to=phone_number, channel='sms')
    return Response(status=200, data={'message': 'User is registered'})  


@api_view(['POST'])
def verify_otp(request):
  if request.method == "POST":
    otp_data = request.data
    phone_number = otp_data.get("Mobile_Number")
    print('inside') 
    print(phone_number)
    otp = otp_data.get('Entered_Otp')
    print(otp)
    # verification_check = client.verify.v2.services(settings.TWILIO_VERIFY_SERVICE_ID) \
    #     .verification_checks \
    #     .create(to=phone_number, code=otp)

    # if verification_check.status == "approved":
    return Response(status=200)

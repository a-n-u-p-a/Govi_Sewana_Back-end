from django.shortcuts import render, redirect
from django.conf import settings
from twilio.rest import Client
from django.http import HttpResponse
import logging
logger = logging.getLogger(__name__) 

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
    print(phone_number)
    # verification = client.verify.v2.services(settings.TWILIO_VERIFY_SERVICE_ID) \
    #     .verifications \
    #     .create(to=phone_number, channel='sms')
    if settings.TESTING_MODE:
        logger.debug("Testing Mode: Skipping OTP sending.")
        request.session['phone_number'] = phone_number
        print(request.session.get('phone_number'))
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
          return Response({"success": True})

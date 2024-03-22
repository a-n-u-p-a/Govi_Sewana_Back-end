from django.conf import settings
from twilio.rest import Client
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import user_collection


client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

@api_view(['POST'])
def register_details(request):
  if request.method == "POST":
    registration_data = request.data
    full_name = registration_data.get("Full_Name")
    nic = registration_data.get("NIC")
    phone_number = registration_data.get("Mobile_Number")

    print(user_collection.find_one())
    # Check if a user with the given mobile number already exists
    phone_number = str(phone_number)
    # Prepare two versions of the phone number
    if phone_number.startswith('+94') and not phone_number.startswith('+940'):
      phone_number_alt = phone_number.replace('+94', '+940', 1)
      print(phone_number_alt)
    elif phone_number.startswith('+940'):
      phone_number_alt = phone_number.replace('+940', '+94', 1)
      print(phone_number_alt)

    # Update the query to look for either version of the phone number
    existing_number = user_collection.find_one({
        "$or": [
            {"Mobile_Number": phone_number},
            {"Mobile_Number": phone_number_alt}
        ]
    })
    existing_nic = user_collection.find_one({"NIC": nic})
    if existing_number or existing_nic:
      print('user already exists')
      # If a user exists, return a response indicating the user is already registered
      return Response(status=409, data={'message': 'User is already registered'})


    # If no existing user is found, insert the new user
    user_collection.insert_one(registration_data)

    print(full_name)
    print(nic)
    print(phone_number)
    # user_collection.insert_one(registration_data)
    # verification = client.verify.v2.services(settings.TWILIO_VERIFY_SERVICE_ID) \
    #     .verifications \
    #     .create(to=phone_number, channel='sms')
    return Response(status=200, data={'message': 'User registered successfully'})  



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

from django.conf import settings
from twilio.rest import Client
import os

class MessageHandler:

    phone_number = None
    otp = None

    def __init__(self, phone_numeber,otp) -> None:
        self.phone_number = phone_numeber
        self.otp = otp

    def send_otp_on_phone(self):
        # Find your Account SID and Auth Token at twilio.com/console
        # and set the environment variables. See http://twil.io/secure
        account_sid = os.environ['ACe840552748ca0a1155df212e41305801']
        auth_token = os.environ['315ae331a642b88c8d7324ab1e639369']
        client = Client(account_sid, auth_token)

        verification = client.verify \
                            .v2 \
                            .services('VAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX') \
                            .verifications \
                            .create(to='+94761636002', channel='sms')

        print(verification.sid)

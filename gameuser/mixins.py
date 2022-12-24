from http import client
import random
from django.conf import settings
from twilio.rest import Client

class MessageHandler:
    phone_number = None
    otp          = None
    def __init__(self, phone_number, otp) -> None:
        self.phone_number = phone_number
        self.otp          = otp

    def send_otp_to_phone(self):
        client = Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
        verification = client.verify \
                     .v2 \
                     .services('VA6f47961f8a9199b359c2d9d40b23da7e') \
                     .verifications \
                     .create(to=self.phone_number, channel='sms')

    def validate(self):
        client=Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
        verification_check = client.verify \
                           .v2 \
                           .services('VA6f47961f8a9199b359c2d9d40b23da7e') \
                           .verification_checks \
                           .create(to=self.phone_number,code=self.otp)
        validation=verification_check.status
        print(  validation)
        return validation    
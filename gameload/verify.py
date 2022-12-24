
import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.conf import settings



client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN )
verify = client.verify.services(settings.SERVICE_ID)


def send(phone):
    if '+91' in phone:
        verify.verifications.create(to=phone, channel='sms')
    else:
         verify.verifications.create(to=str('+91')+phone, channel='sms')
    


def checked(phone, code):
    try:
        result = verify.verification_checks.create(to=('+91')+phone, code=code)
        print(result)
    except TwilioRestException:
        return False
    return result.status == 'approved'
    pass
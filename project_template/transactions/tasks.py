from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.conf import settings

import twilio
import twilio.rest


@shared_task
def send_twilio_message(to_number, otp):
    client = twilio.rest.TwilioRestClient(
        settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    return client.messages.create(
        body="one-time password for xyz is %s" % otp,
        to=to_number,
        from_=settings.TWILIO_DEFAULT_CALLERID
    )

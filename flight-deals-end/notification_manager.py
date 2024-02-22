from twilio.rest import Client

TWILIO_SID = "AC0c9d8165cc10ca5a15bef271e14044ab"
TWILIO_AUTH_TOKEN = "ad083c98a2402e603b2986e5eb094d9c"
TWILIO_VIRTUAL_NUMBER = '+19062144306'
TWILIO_VERIFIED_NUMBER = '+254715371294'


class NotificationManager:

    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_VERIFIED_NUMBER,
        )
        # Prints if successfully sent.
        print(message.sid)
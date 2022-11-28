from decouple import config
import os
from twilio.rest import Client

account_sid = config('TWILIO_ACCOUNT_SID')
auth_token = config('TWILIO_AUTH_TOKEN')
twilio_phone = config("TWILIO_PHONE_NUMBER")

client = Client(account_sid, auth_token)


def send_order_information(order_information):

    # {
    #     'amount': 3000,
    #     'phone_number': 'string',
    #     'address': 'string',
    #     'order_detail': 'string',
    #     'completed': True,
    #     'payment_method': 'string',
    #     'trx_ref': 'string',
    #     'user': UUID('6f2c2af8-5cb1-4db2-9489-208456022010'),
    #     'vendor': UUID('0e4f3ab4-93bd-47c0-9a8d-b90fcefef507')
    # }

    print(order_information)

    body = order_information
    message = client.messages.create(body=body,
                                     from_=f"whatsapp:" + twilio_phone,
                                     to='whatsapp:+2348179120615')

    print(message.sid)


def track_order(information):

    if information.message in ['sent', 'hi', '1', '2', '3']:
        pass

    message = client.messages.create(body=body,
                                     from_=f"whatsapp:" + twilio_phone,
                                     to='whatsapp:+2348179120615')

    print(message.sid)


# send_order_information()
# def send_order_information(order_information):
# 	print(twilio_phone)
# 	message = client.messages.create(
# 								body='Hello',
# 								from_=f"whatsapp:"+twilio_phone,
# 								to='whatsapp:+2348179120615'
# 							)

# 	print(message.sid)

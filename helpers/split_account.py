import requests
from decouple import config

api_url = "https://api.paystack.co/subaccount/"
api_url2 = "https://api.flutterwave.com/v3/subaccounts"

params = {
    'business_name': "Emmy Ventures",
    'settlement_bank': "50211",
    'account_number': "2009367126",
    'percentage_charge': 3.84615385,
}

param_flutterwave = {
    "account_bank": "044",
    "account_number": "0690000037",
    "business_name": "Eternal Blue",
    "business_mobile": "09087930450",
    "split_type": "percentage",
    "split_value": 0.2
}


def create_split_account(account_details):
    auth_token = config("FLUTTER_TEST_SK")
    hed = {'Authorization': 'Bearer ' + auth_token}

    url = api_url
    response = requests.post(url, json=account_details, headers=hed)
    print(response)
    print(response.json())
    return response.json()


# create_split_account(params)


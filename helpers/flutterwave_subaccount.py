import os
from decouple import config
from rave_python import Rave, Misc, RaveExceptions

publicKey = config("FLW_PUBLIC_KEY")
secretKey = config("RAVE_SECRET_KEY")

# rave = Rave(publicKey, secretKey, usingEnv=False)
rave = Rave(publicKey, secretKey, usingEnv=False)

details = {
    "account_bank": "044",
    "account_number": "0690000037",
    "business_name": "Flutterwave Developers",
    "business_mobile": "09087930450",
    "country": "NG",
    "split_type": "percentage",
    "split_value": 0.2
}


def create_subaccount(data, current_vendor):
    try:
        data['business_name'] = current_vendor.name
        data['business_mobile'] = current_vendor.phone_number
        data["split_type"] = "percentage"
        data["split_value"] = 0.2
        data["business_email"] = current_vendor.email
        data["business_contact"] = current_vendor.phone_number
        data['business_contact_mobile'] = current_vendor.phone_number
        data["country"] = "NG"
        response = rave.SubAccount.create(data)
        # print(response)
        return response
    except RaveExceptions.SubaccountCreationError as e:
        # print("Error Message 1 from Function", e.err)
        # print("Error Message 2 from Function", e.err)
        return e.err
    except RaveExceptions.IncompletePaymentDetailsError as e:
        # print("Error Message 3 from Function", e)
        return e.err

    except RaveExceptions.PlanStatusError as e:
        # print("Error Message 4 from Function", e.err)
        return e.err

    except RaveExceptions.ServerError as e:
        # print("Error Message 5 from Function", e.err)
        return e.err

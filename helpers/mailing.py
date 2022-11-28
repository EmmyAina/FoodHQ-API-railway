from authentication.models import Token, OTPToken, PasswordResetToken
from django.core.mail import send_mail
from rest_framework import status
from sentry_sdk import capture_exception
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from random import randint


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def send_verification_token(user):
    try:
        # token, _ = Token.objects.update_or_create(
        #     user=user, token_type='ACCOUNT_VERIFICATION',
        #     defaults={'user': user, 'token_type': 'ACCOUNT_VERIFICATION', 'token': get_random_string(120)})
        token, _ = OTPToken.objects.update_or_create(
            user=user, token_type='ACCOUNT_VERIFICATION',
            defaults={'user': user, 'token_type': 'ACCOUNT_VERIFICATION', 'token': random_with_N_digits(4)})
        send_mail("Account Verification Mail",
                  f'Use the token below to verify your newly registered account {token.token}',
                  "ainae06@gmail.com",
                  [f'{token.user.email}'],
                  fail_silently=False,

                  )
        return Response(
            {'message': f'Verification mail sent to {token.user.email}'}, status=status.HTTP_200_OK
        )
    except Exception as e:
        capture_exception(e)
        return Response({'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

def send_password_reset_token(user):
    try:
        # token, _ = Token.objects.update_or_create(
        #     user=user, token_type='ACCOUNT_VERIFICATION',
        #     defaults={'user': user, 'token_type': 'ACCOUNT_VERIFICATION', 'token': get_random_string(120)})
        token, _ = PasswordResetToken.objects.update_or_create(
            user=user, token_type='PASSWORD_RESET', 
            defaults={'user': user,"has_been_confirmed":False, 'token_type': 'PASSWORD_RESET','token': random_with_N_digits(4)})
        send_mail("Password Reset Mail",
                  f'Use the token below to reset your account password {token.token}',
                  "ainae06@gmail.com",
                  [f'{token.user.email}'],
                  fail_silently=False,
                  )
        return Response(
            {'message': f'Password Reset mail send to {token.user.email}'}, status=status.HTTP_200_OK
        )
    except Exception as e:
        capture_exception(e)
        return Response({'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
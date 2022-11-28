from authentication.models import User, Token
from rest_framework_simplejwt.tokens import RefreshToken


def refresh_access_token(user):
    tokens = RefreshToken.for_user(user)
    payload = {
        'user_id': user.id,
        'refresh': str(tokens),
        'access': str(tokens.access_token)
    }
    token, _ = Token.objects.update_or_create(user=user,
                                              token_type='AUTH_TOKEN',
                                              defaults={
                                                  'user': user,
                                                  'token': 'jwt_token',
                                                  'token_type': 'AUTH_TOKEN',
                                                  'refresh':
                                                  payload['refresh'],
                                                  'access': payload['access']
                                              })

    return payload

from django.contrib import admin
from .models import Token, User, OTPToken, PasswordResetToken

# Register your models here.

# Register your models here.
admin.site.register((User, Token, OTPToken, PasswordResetToken))

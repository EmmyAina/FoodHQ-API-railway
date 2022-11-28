from django.contrib import admin
from .models import AppWallet, WalletTrxInformation, IncomingPayment

# Register your models here.
admin.site.register((AppWallet, WalletTrxInformation, IncomingPayment))

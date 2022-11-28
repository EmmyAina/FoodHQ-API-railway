import uuid
from datetime import datetime, timedelta, timezone
# from business.models import VendorInformation
from authentication.models import User
from django.db import models
from rest_framework import status

from rest_framework.response import Response


TX_TYPE = [
 ('debit', 'Debit'),
 ('credit', 'Credit'),
 ('reversal', 'Reversal'),
 ('promo', 'promo'),
]

class AppWallet(models.Model):
    id = models.OneToOneField(
     User, related_name='wallet', on_delete=models.CASCADE, primary_key=True,)
    current_balance = models.IntegerField(default=0, )
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id.email} ₦{self.current_balance} {self.id.id}'

    class Meta:
        verbose_name_plural = "App Wallet"

    def credit_account(self, amount_to_credit):
        self.current_balance = self.current_balance + amount_to_credit
        self.save()
        return Response({"message": "Account Credited Successfully"}, status=status.HTTP_200_OK)


    def debit_account(self, amount_to_debit):
        if  amount_to_debit <= 0:
            pass
        elif amount_to_debit > self.current_balance:
            pass
        else:
            self.current_balance = self.current_balance - amount_to_debit
            self.save()
            return Response({"message": "Account Debited Successfully"}, status=status.HTTP_200_OK)

class WalletTrxInformation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.IntegerField()
    transaction_type = models.CharField(
     choices=TX_TYPE, blank=True, max_length=100,)
    user = models.ForeignKey(User,
           on_delete=models.CASCADE)
    transaction_reference = models.CharField(blank=True,max_length=16)
    date = models.DateTimeField(auto_now_add=True,)

    _trx_response = {}

    def __str__(self):
        return f"{self.id} {self.user.username} => {self.transaction_type} => {self.amount} "


    class Meta:
        verbose_name_plural = "Wallet Transaction Information"
        ordering = ("-date",)

    def save(self, *args, **kwargs):

        user_wallet_instance = AppWallet.objects.get(id=self.user)
        if self.transaction_type == 'credit':
            self._trx_response = user_wallet_instance.credit_account(amount_to_credit=self.amount)

            super(WalletTrxInformation, self).save(*args, **kwargs)
        elif self.transaction_type == 'debit':
            if self.amount <= 0:
                self._trx_response = Response({"error": "An Error occurred, amount to debit is less than zero"}, status=status.HTTP_400_BAD_REQUEST)
                pass
            elif self.amount > user_wallet_instance.current_balance:
                self._trx_response=  Response({"error": "An Error occurred, amount is greater than current balance"}, status=status.HTTP_400_BAD_REQUEST)
                pass
            else:
                self._trx_response = user_wallet_instance.debit_account(amount_to_debit=self.amount)
                super(WalletTrxInformation, self).save(*args, **kwargs)

    @property
    def trx_response(self):
        return self._trx_response

class IncomingPayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trx_ref = models.CharField(max_length=50, blank=False)
    user_email = models.EmailField(max_length=50, blank=False)
    message = models.TextField(max_length=10000)
    status = models.CharField(max_length=20, blank=False)
    amount = models.IntegerField()
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    payment_confirmed = models.BooleanField(default=False)

    def update_payment_status(self):
        self.payment_confirmed = True
        self.save()

    def __str__(self):
        return f"{self.id} {self.user_email} => {self.date_updated} => {self.amount} "

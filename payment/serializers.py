from django.db import models
from .models import AppWallet, WalletTrxInformation, IncomingPayment
from rest_framework import serializers


class AmountCollectionSerializer(serializers.Serializer):
    amount = serializers.IntegerField()


class IncomingTRXSerializer(serializers.ModelSerializer):

    class Meta:
        model = IncomingPayment
        # exclude = ("payment_confirmed", )
        fields = "__all__"
        extra_kwargs = {"payment_confirmed": {"read_only": True}}


class AppWalletSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%d-%b-%Y %H:%M")

    class Meta:
        model = AppWallet
        fields = "__all__"


class WalletTrxSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%d-%b-%Y %H:%M")

    class Meta:
        model = WalletTrxInformation
        exclude = ("user", )

    def create(self, validated_data):

        trx_instance = WalletTrxInformation(**validated_data)
        trx_instance.save()

        transaction_response = trx_instance.trx_response
        return transaction_response

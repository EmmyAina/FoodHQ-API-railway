from decouple import config
from django.shortcuts import render
from helpers.custom_permissions import IsStaff
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from sentry_sdk import capture_exception

from .models import AppWallet, WalletTrxInformation
from .serializers import (AmountCollectionSerializer, AppWalletSerializer,
                          WalletTrxSerializer, IncomingTRXSerializer)


# Create your views here.
class AppWalletViewset(ModelViewSet):
    serializer_class = AppWalletSerializer
    queryset = AppWallet.objects.all()
    permission_classes = [
        AllowAny,
    ]

    @action(methods=["POST"],
            url_path="save-pending-transaction",
            detail=False,
            serializer_class=IncomingTRXSerializer,
            permission_classes=[
                AllowAny,
            ])
    def save_pending_transaction(self, request, *args, **kwargs):
        """
		Endpoint for saving incoming transaction before confirmation incase of errors

		#
		"""
        try:
            data = request.data
            serialized_data = self.serializer_class(data=data)
            serialized_data.is_valid(raise_exception=True)

            serialized_data.save()

            return Response(serialized_data.data)
        except Exception as e:
            capture_exception(e)
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'],
            url_path='credit-account',
            detail=False,
            serializer_class=AmountCollectionSerializer,
            permission_classes=[
                IsAuthenticated,
            ])
    def credit_account(self, request, *args, **kwargs):
        """
		Endpoint for crediting a user wallet account

		#
		"""
        try:
            data = request.data
            user_wallet_instance = self.queryset.get(id=self.request.user.id)
            user_wallet_instance.credit_account(
                amount_to_credit=data['amount'])

            serialized_data = AppWalletSerializer(user_wallet_instance)
            return Response(serialized_data.data)
        except Exception as e:
            capture_exception(e)
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'],
            url_path='debit-account',
            detail=False,
            serializer_class=AmountCollectionSerializer,
            permission_classes=[
                IsAuthenticated,
            ])
    def debit_account(self, request, *args, **kwargs):
        """
		Endpoint for debiting a user wallet account

		#
		"""
        try:
            data = request.data
            user_wallet_instance = self.queryset.get(id=self.request.user.id)
            user_wallet_instance.debit_account(amount_to_debit=data['amount'])

            serialized_data = AppWalletSerializer(user_wallet_instance)
            return Response(serialized_data.data)
        except Exception as e:
            capture_exception(e)
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=["GET"],
            url_path='wallet-information',
            detail=False,
            serializer_class=AppWalletSerializer,
            permission_classes=[IsAuthenticated])
    def fetch_wallet_information(self, request, *args, **kwargs):
        try:
            user_wallet_instance = self.queryset.get(id=self.request.user.id)
            serialized_data = AppWalletSerializer(user_wallet_instance).data

            user_trx_information = WalletTrxInformation.objects.filter(
                user=self.request.user.id)
            serialized_trx_info = WalletTrxSerializer(user_trx_information,
                                                      many=True).data
            serialized_data["trx_info"] = serialized_trx_info
            return Response(serialized_data)
        except Exception as e:
            capture_exception(e)
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'],
            url_path='save-transaction',
            detail=False,
            serializer_class=WalletTrxSerializer,
            permission_classes=[
                IsAuthenticated,
            ])
    def save_transaction(self, request, *args, **kwargs):
        """
		Endpoint for debiting a user wallet account

		#
		"""
        try:
            data = request.data
            data["user"] = self.request.user
            trx_instance = self.serializer_class.create(self,
                                                        validated_data=data)

            user_wallet_instance = self.queryset.get(id=self.request.user.id)
            serialized_data = AppWalletSerializer(user_wallet_instance)

            return trx_instance
        except Exception as e:
            capture_exception(e)
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)

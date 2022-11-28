from django.shortcuts import render
from helpers.custom_permissions import IsStaff
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from sentry_sdk import capture_exception

from .models import OrderInformation
from .serializers import OrderinformationSerializer, OrderinformationListSerializer
from business.models import VendorInformation
from helpers.messaging import send_order_information, track_order

from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from decouple import config


# Create your views here.
class OrderInformationViewSet(ModelViewSet):
    serializer_class = OrderinformationSerializer
    queryset = OrderInformation.objects.all()
    permission_classes = [
        AllowAny,
    ]

    def get_serializer_class(self):
        if self.action in ["list", "fetch_user_orders"]:
            return OrderinformationListSerializer
        # elif self.action == "create":
        #     return OrderinformationSerializer
        # elif self.action == "vendor_profile":
        #     return OrderinformationSerializer
        # elif self.action in ["put", "patch", "delete", "complete_order"]:
        #     return OrderinformationSerializer
        # elif self.action in ["add_item", "vendor_menu"]:
        #     return OrderinformationSerializer
        else:
            return OrderinformationSerializer

    def create(self, request, *args, **kwargs):
        """
		Endpoint for saving a recently placed order

		This endpoint saves an order information right after payment is completed by the user
		"""
        try:
            data = request.data
            serialized_data = self.serializer_class(data=data)
            serialized_data.is_valid(raise_exception=True)

            self.serializer_class.create(self, validated_data=data)
            order_message = serialized_data.data['message']
            return_info = serialized_data.data

            # print("Vendor Info ==> ", request.data['vendor'].phone_number)

            send_order_information(order_message)
            return_info["vendor_phone"] = request.data['vendor'].phone_number
            return_info["message"] = "Order placed Successfully"
            return_info["status"] = status.HTTP_200_OK

            return Response(return_info)
        except Exception as e:
            capture_exception(e)
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'],
            url_path='complete-order',
            detail=True,
            serializer_class=OrderinformationSerializer,
            permission_classes=[
                AllowAny,
            ])
    def complete_order(self, request, pk=None, *args, **kwargs):
        """
		Endpoint for completing user order

		This endpoint marks the user order as completed once the order has been sent out or delivered
		"""
        try:
            order_instance = self.queryset.get(id=pk)
            order_instance.complete_order()

            serialized_data = self.serializer_class(order_instance)
            return Response(serialized_data.data)
        except Exception as e:
            capture_exception(e)
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'],
            url_path='vendor/fetch-orders',
            detail=True,
            serializer_class=OrderinformationSerializer,
            permission_classes=[])
    def fetch_vendor_orders(self, request, pk=None, *args, **kwargs):
        """
		Endpoint for fetching order information for a single vendor

		This endpoint fetches all order history belonging to a specific vendor
		"""
        try:
            data = request.data
            order_instance = self.queryset.filter(vendor=pk)

            serialized_data = self.serializer_class(order_instance, many=True)
            return Response(serialized_data.data)
        except Exception as e:
            capture_exception(e)
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=["GET"],
            url_path="user/fetch-orders",
            detail=False,
            serializer_class=OrderinformationListSerializer,
            permission_classes=[
                IsAuthenticated,
            ])
    def fetch_user_orders(self, request, *args, **kwargs):
        """
		Endpoint for fetching order information for a user

		#
		"""
        try:
            current_user_id = self.request.user.id

            orders_instance = self.queryset.filter(user=current_user_id)

            serialized_data = self.serializer_class(orders_instance, many=True)
            return Response(serialized_data.data)
        except Exception as e:
            capture_exception(e)
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    @action(methods=["GET", "POST"],
            url_path='handle-message',
            detail=False,
            serializer_class=None)
    def handle_message(self, request, *args, **kwargs):
        payload = request.data

        print("Twilio Response => ", payload)

        vendor_phone = payload['From'].strip("whatsapp:")
        vendor_id = VendorInformation.objects.get(phone_number=vendor_phone).id
        print((vendor_id))

        latest_order_from_vendor = self.queryset.filter(
            vendor=vendor_id).latest('date')

        print(latest_order_from_vendor)

        return Response({"message": 'Received'})


# class OrderTransaction(GenericAPIView):
#     """
#     Endpoint for verifying a new user's email address before login

#     This endpoint send a verification link to the registered email address
#     """
#     serializer_class = OrderHistorySerializer
#     permission_class = (AllowAny,)
#     my_tags = ['Order']

#     def post(self, request):
#         data = request.data
#         serialized_data = self.serializer_class(data=data)
#         serialized_data.is_valid(raise_exception=True)

#         self.serializer_class.create(self, validated_data=data)
#         return Response(serialized_data.data)

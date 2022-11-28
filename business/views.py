from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from helpers.custom_permissions import IsStaff
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from sentry_sdk import capture_exception

from .models import VendorInformation, MenuItems
from helpers.flutterwave_subaccount import create_subaccount
from .serializers import (VendorInformationSerializer, MenuItemSerializer,
                          VendorProfileSerializer,
                          VendorInformationListSerializer,
                          RegisterVendorBankSerializer)


class BusinessViewSet(ModelViewSet):
    serializer_class = VendorInformationSerializer
    queryset = VendorInformation.objects.all()
    permission_classes = [
        AllowAny,
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return VendorInformationListSerializer
        elif self.action == "create":
            return VendorInformationSerializer
        elif self.action == "vendor_profile":
            return VendorProfileSerializer
        elif self.action in ["put", "patch", "delete"]:
            return VendorInformationSerializer
        elif self.action in ["add_item", "vendor_menu"]:
            return MenuItemSerializer
        elif self.action in ["vendor_bank"]:
            return RegisterVendorBankSerializer
        else:
            return VendorInformationSerializer

    # @action(methods=['POST'], url_path='register-vendor', serializer_class=VendorInformationSerializer, detail=False)

    def create(self, request, *args, **kwargs):
        """
		Endpoint for creating a new vendor

		This endpoint create a new vendor and a user account associated with the vendor
		"""
        # try:
        # 4674
        data = request.data
        # print("Data Queryset  => ", data)

        # category_list = data['email']
        # print("category list => ", )

        # data = data.dict()
        # data['category'] = category_list

        # print("Data Dict => ", data)
        data['email'] = data['email'].lower()
        serialized_data = self.serializer_class(data=data)
        serialized_data.is_valid(raise_exception=True)
        self.serializer_class.create_user(self, validated_data=data)
        self.serializer_class.create(self, validated_data=data)
        return Response(
            {
                'message':
                'Account Registerd Successfully, please check email for validation'
            },
            status=status.HTTP_201_CREATED)
        # except Exception as e:
        #     capture_exception(e)
        #     return Response({"error": str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'],
            url_path='menu',
            serializer_class=MenuItemSerializer,
            detail=False,
            permission_classes=[
                IsStaff,
            ])
    def add_item(self, request, *args, **kwargs):
        """
		Endpoint for adding an item to a vendor's menu

		This endpoint is used to add a new item to a vendor's menu
		"""
        try:
            data = request.data
            serialized_data = self.serializer_class(data=data)
            serialized_data.is_valid(raise_exception=True)

            self.serializer_class.create(self,
                                         user=self.request.user,
                                         validated_data=data)

            return Response(serialized_data.data)
        except Exception as e:
            capture_exception(e)
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'],
            url_path='vendor-profile',
            serializer_class=VendorProfileSerializer,
            detail=False,
            permission_classes=[],
            parser_classes=(FormParser, MultiPartParser))
    def vendor_profile(self, request, *args, **kwargs):
        """
		Endpoint for updating a vendor's profile

		This endpoint is used to update a vendor's profile by adding additional information like category, profile picture etc...
		"""
        try:
            data = request.data
            current_vendor = self.queryset.get(user=self.request.user)

            serialized_data = self.serializer_class(data=data)
            serialized_data.is_valid(raise_exception=True)

            current_vendor = self.queryset.get(user=self.request.user)
            resp = current_vendor.update_vendor_profile(data)

            return Response({"message": f'{resp}'})
        except Exception as e:
            capture_exception(e)
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'],
            detail=True,
            url_path='menu',
            serializer_class=MenuItemSerializer)
    def vendor_menu(
        self,
        request,
        pk=None,
        *args,
        **kwargs,
    ):
        """
		Endpoint for fetching a vendor's menu list
		"""
        try:
            menu_item_data = MenuItems.objects.all().filter(vendor=pk)
            serialized_data = self.serializer_class(menu_item_data, many=True)

            return Response(serialized_data.data)
        except Exception as e:
            capture_exception(e)
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=["POST"],
            detail=False,
            url_path="register-bank-account",
            serializer_class=RegisterVendorBankSerializer,
            permission_classes=[IsStaff])
    def vendor_bank(self, request, *args, **kwargs):
        try:
            current_vendor = self.queryset.get(user=self.request.user)

            data = request.data
            serialized_data = self.serializer_class(data=data)
            serialized_data.is_valid(raise_exception=True)

            subaccount = create_subaccount(data, current_vendor)

            print("The SucAccount ====> ", subaccount)

            if subaccount['error'] == False:
                current_vendor.update_vendor_subaccount(
                    subaccount['data']['subaccount_id'])
                return Response(subaccount)
            else:
                return Response(subaccount)

        except Exception as e:
            capture_exception(e)
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)

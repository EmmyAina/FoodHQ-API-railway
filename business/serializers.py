from django.db import models
from .models import VendorInformation, MenuItems, Category
from rest_framework import serializers
from authentication.models import User
from authentication.serializers import UserRegistrationSerializer


def required(value):
    if value is None:
        raise serializers.ValidationError("This field is required")


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class VendorInformationSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()
    category = CategorySerializer(read_only=True, many=True)
    opening_time = serializers.TimeField(input_formats=[
        '%H:%M',
    ])
    closing_time = serializers.TimeField(input_formats=[
        '%H:%M',
    ])

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True, many=True)

    class Meta:
        model = VendorInformation
        exclude = ("user", "file", "address", "profile_updated")

    def create_user(self, validated_data):
        required_user_info = {
            "email": validated_data.get('email'),
            "username": validated_data.get('name'),
            "phone_number": validated_data.get('phone_number'),
            "password": validated_data.get('password'),
            "is_staff": True
        }
        return UserRegistrationSerializer.create(
            self, validated_data=required_user_info)

    def create(self, validated_data):
        validated_data.pop("csrfmiddlewaretoken", None)
        validated_data.update(
            {"user": User.objects.get(email=validated_data.get('email'))})
        validated_data.pop('password')
        # validated_data['category'] =(id=validated_data['category'])
        categories = validated_data.pop('category_id')

        vendor_instance = VendorInformation.objects.create(**validated_data)

        print("Vendor Instance ====> ", vendor_instance.category)

        # for item in categories:
        vendor_instance.category.add(*categories)
        vendor_instance.save()

        return vendor_instance


class VendorInformationListSerializer(serializers.ModelSerializer):
    opening_time = serializers.DateTimeField(format="%H:%M")
    closing_time = serializers.DateTimeField(format="%H:%M")

    class Meta:
        model = VendorInformation
        exclude = ("user", )


class VendorInformationForOrder(serializers.ModelSerializer):

    class Meta:
        model = VendorInformation
        fields = ("name", "id", "file")


class MenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuItems
        exclude = ('vendor', )

    def create(self, user, validated_data):
        validated_data['vendor'] = VendorInformation.objects.get(user=user.id)
        menu_item_instace = MenuItems(**validated_data)
        menu_item_instace.save()

        return menu_item_instace


class VendorProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorInformation
        fields = [
            "file",
            "address",
            "category",
        ]

    def get_file(self, instance):
        # returning image url if there is an image else blank string
        return instance.file.url if instance.file else ''


class RegisterVendorBankSerializer(serializers.Serializer):
    account_bank = serializers.CharField(max_length=20, validators=[required])
    account_number = serializers.CharField(max_length=20,
                                           validators=[required])

from django.db import models
from .models import User, OrderInformation
from rest_framework import serializers
from business.models import VendorInformation
from payment.models import IncomingPayment
from business.serializers import VendorInformationForOrder
import random, string


def order_id_generator(size):
    x = ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase +
                      string.digits) for _ in range(size))
    return f"FDHQ-{x}".upper()


class OrderinformationSerializer(serializers.ModelSerializer):
    # date = serializers.DateTimeField(format="%d-%b-%Y %H:%M")
    transaction_id = serializers.CharField()

    class Meta:
        model = OrderInformation
        fields = "__all__"

    def create(self, validated_data):
        validated_data['user'] = User.objects.get(id=validated_data['user'])
        # validated_data['order_id'] = order_id_generator(5)

        current_vendor = VendorInformation.objects.get(
            id=validated_data['vendor'])
        tranx_info = IncomingPayment.objects.get(
            id=validated_data['transaction_id'])
        validated_data['vendor'] = current_vendor

        validated_data["phone_number"] = "+234" + validated_data[
            "phone_number"].strip("0")

        validated_data.pop("transaction_id", None)
        order_info_instance = OrderInformation(**validated_data)

        order_info_instance.save()
        current_vendor.update_order_count()
        tranx_info.update_payment_status()
        # print("Order History Saved")
        return "Order History Saved"


class OrderinformationListSerializer(serializers.ModelSerializer):
    vendor = VendorInformationForOrder()
    date = serializers.DateTimeField(format="%d-%b-%Y %H:%M")

    class Meta:
        model = OrderInformation
        fields = "__all__"

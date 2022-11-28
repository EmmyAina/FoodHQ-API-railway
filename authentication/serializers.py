from django.db import models
from django.utils.translation import gettext_lazy as _
from helpers.mailing import send_verification_token
from rest_framework import serializers
from payment.models import AppWallet
from .models import User


def required(value):
    if value is None:
        raise serializers.ValidationError("This field is required")


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "phone_number",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user_instance = User(**validated_data)
        if password != None:
            user_instance.set_password(password)

        user_instance.save()

        new_wallet = AppWallet(id=user_instance)
        new_wallet.save()
        return send_verification_token(user_instance)

        # return user_instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=225, validators=[required])
    password = serializers.CharField(
        validators=[required],
        label=_("Password"),
        style={"input_type": "password"},
        max_length=225,
        write_only=False,
    )


class VerifyAccountSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=300, validators=[required])


class OTPVerifyAccountSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=6, validators=[required])


class UpdateUsernameSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20, validators=[required])

class SendPasswordResetSerializer(serializers.Serializer):
       email = serializers.EmailField(max_length=225, validators=[required])

class ResetPasswordSerializer(serializers.Serializer):
	password = serializers.CharField(max_length=20, validators=[required])
	token = serializers.CharField(max_length=4, validators=[required])


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=20, validators=[required])
    new_password = serializers.CharField(max_length=20, validators=[required])

from helpers.login_token import refresh_access_token
from helpers.mailing import send_verification_token,send_password_reset_token
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from sentry_sdk import capture_exception

from .models import Token, User, OTPToken, PasswordResetToken
from .serializers import (LoginSerializer, UserRegistrationSerializer,
                          VerifyAccountSerializer, OTPVerifyAccountSerializer,UpdateUsernameSerializer,ChangePasswordSerializer,
                          SendPasswordResetSerializer,ResetPasswordSerializer)


# Create your views here.
class AuthViewset(ModelViewSet):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()
    permission_classes = [
        AllowAny,
    ]

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in [
                "create",
                "partial_update",
        ]:
            permission_classes = [
                AllowAny,
            ]
        elif self.action in ["list", "change_password"]:
            permission_classes = [
                IsAuthenticated,
            ]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.action in ['login', 'register', 'send_reset_token']:
            return self.queryset
        elif self.action in [ "reset_password", "confirm_reset_token"]:
            return PasswordResetToken.objects.all()
        elif self.action in ['verify_account']:
            return OTPToken.objects.all()

        # REGISTERATION ENDPOINT

    # @action(
    # 	methods=["POST"],
    # 	url_path="register",
    # 	detail=False,
    # 	serializer_class=UserRegistrationSerializer,
    # )
    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            # data._mutable = True
            data['email'] = data['email'].lower()
            data['username'] = data['username'].capitalize()
            # data._mutable = False

            serialized_data = self.serializer_class(data=request.data)
            serialized_data.is_valid(raise_exception=True)
            serialized_data.save()
            return Response({"message": 'Verification Message sent successfully'})
        except Exception as e:
            capture_exception(e)
            if e.detail['email']:
                return Response({"error": "Enter a valid email address."},
                                status.HTTP_400_BAD_REQUEST)
            return Response({"error": str(e)},
                            status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        user = self.queryset.filter(id=self.request.user.id).first()
        serialized_data = self.serializer_class(user)
        return Response(serialized_data.data)

    # LOGIN ENDPOINT
    @action(
        methods=["POST"],
        url_path="login",
        detail=False,
        serializer_class=LoginSerializer,
    )
    def login(self, request, *args, **kwargs):
        try:
            data = request.data
            user = self.get_queryset().filter(
                email=data["email"].lower()).first()
            if not user:
                return Response(
                    {
                        "error":
                        "Invalid Login Crednetials. (User Not Found) remove later",
                        "status": status.HTTP_401_UNAUTHORIZED
                    },
                    status.HTTP_401_UNAUTHORIZED
                )
            # Check if password is correct
            if not user.check_password(request.data.get("password", None)):
                return Response(
                    {
                        "error":
                        "Invalid Login Crednetials. (Password issue) remove later",
                        "status": status.HTTP_401_UNAUTHORIZED

                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
            # Check if account has been verified
            if not user.verified:
                send_verification_token(
                    self.get_queryset().filter(email=data["email"]).first())
                return Response({'error': 'Account not verifified. Check Mail(Resend verification link)', 'status': status.HTTP_401_UNAUTHORIZED}, status = status.HTTP_401_UNAUTHORIZED)
            payload = refresh_access_token(user)

            return Response({
                "access": payload["access"],
                "refresh": payload["refresh"]
            })
        except Exception as e:
            capture_exception(e)
            return Response({"error": str(e)},
                            status.HTTP_400_BAD_REQUEST
                            )

    @action(methods=['POST'], url_path='verify-account', detail=False, serializer_class=VerifyAccountSerializer)
    def verify_account(self, request, *args, **kwargs):
        try:
            serialized_data = self.serializer_class(data=request.data)
            serialized_data.is_valid(raise_exception=True)

            received_token = request.data.get('token')

            token = self.get_queryset().filter(token=received_token).first()

            if token and token.is_valid():
                token.verify_user()
                token.delete()
                return Response({'message': 'Account Verified Successfully'}, status.HTTP_200_OK)
            else:
                return Response(
                    {"error": 'Invalid or Expired Verification Token',
                        'status': status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            capture_exception(e)
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], url_path='send-reset-token', detail=False, serializer_class=SendPasswordResetSerializer)
    def send_reset_token(self, request, *args, **kwargs):
        """
            Endpoint for sending password reset token to email address

            #
            """
        try:
            serialized_data = self.serializer_class(data=request.data)
            serialized_data.is_valid(raise_exception=True)

            received_email = request.data.get('email')

            user_instance = self.get_queryset().filter(email=received_email).first()

            if user_instance:
                return send_password_reset_token(user_instance)
            else:
                return Response(
                    {"error": 'User not found',
                        'status': status.HTTP_400_BAD_REQUEST},status = status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            capture_exception(e)
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], url_path='confirm-reset-token', detail=False, serializer_class=OTPVerifyAccountSerializer)
    def confirm_reset_token(self, request, *args, **kwargs):
        """
        Endpoint for confirming password reset token sent to a user's email 

        #
        """
        try:
            serialized_data = self.serializer_class(data=request.data)
            serialized_data.is_valid(raise_exception=True)

            received_token = request.data.get('token')

            token = self.get_queryset().filter(token=received_token).first()

            if token and token.is_valid():
                token.verify_user()
                # token.delete()
                return Response({'message': 'Email Verified Successfully'}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": 'Invalid or Expired Verification Token',
                        'status': status.HTTP_408_REQUEST_TIMEOUT},status = status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            capture_exception(e)
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], url_path='reset-password', detail=False, serializer_class=ResetPasswordSerializer)
    def reset_password(self, request, *args, **kwargs):
        try:
            serialized_data = self.serializer_class(data=request.data)
            serialized_data.is_valid(raise_exception=True)

            received_token = request.data.get('token', None)

            token = self.get_queryset().filter(token=received_token).first()
            password = request.data.get("password", None)

            if token and token.is_valid() and token.has_been_confirmed:
                token.reset_password(password)
                token.delete()
                return Response(
                    {"message": 'Password Reset Successfully',
                        'status': status.HTTP_200_OK}
                )
            else:
                return Response(
                    {"error": 'Invalid or Expired Verification Token',
                        'status': status.HTTP_408_REQUEST_TIMEOUT}, status = status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            capture_exception(e)
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)


    @action(methods=["POST"], url_path="update-username", detail=False, serializer_class=UpdateUsernameSerializer, permission_classes=[IsAuthenticated])
    def update_username(self, request, *args, **kwargs):
        """
        Endpoint for updating username

        #
        """
        try:
            new_username = request.data['username']
            user_id = self.request.user.id
            current_user_instance = self.queryset.filter(id=user_id).first()
            current_user_instance.update_username(new_username)

            return Response(
                {
                    "message":"Username updated successfully"
                }
            )
        except Exception as e:
            capture_exception(e)
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=["POST"], url_path="change-password", detail=False, serializer_class=ChangePasswordSerializer, permission_classes=[IsAuthenticated])
    def change_password(self, request, *args, **kwargs):
        """
        Endpoint for changing password

        #
        """
        try:
            password_data = request.data
            user_id = self.request.user.id
            current_user_instance = self.queryset.filter(id=user_id).first()
            print(password_data)
            if not current_user_instance.check_password(password_data['old_password']):
                return Response(
                    {
                        "error":
                        "Old password is incorrect",
                        "status": status.HTTP_401_UNAUTHORIZED
                    },
                    status.HTTP_401_UNAUTHORIZED
                )
            else:
                current_user_instance.set_password(password_data["new_password"])
                current_user_instance.save()
                return Response(
                    {
                        "message":"Password changed successfully"
                    }
                )
        except Exception as e:
            capture_exception(e)
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from . import services
from .serializers import UserSerializer, OTPSerializer
from rest_framework.authtoken.models import Token
from .models import User, OneTimePassword
from rest_framework import status
from .services import generate_pin
from rest_framework.exceptions import AuthenticationFailed
import datetime


@api_view(["POST"])
def create_user(request: Request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():

        pin = generate_pin()
        email = request.data["email"]

        services.generate_otp(email=email, pin=pin)

        serializer.save()
        user = User.objects.get(username=request.data["username"])
        user.set_password(request.data["password"])

        user.save()

        token = Token.objects.create(user=user)

        data = {
            "otp": pin,
            "token": token.key,
            "data": serializer.data
        }

        # TODO: Send mail to user containing the otp pin

        return Response(data=data, status=status.HTTP_201_CREATED)

    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request: Request):
    email = request.data["email"]
    password = request.data["password"]

    user = User.objects.filter(email=email).first()
    serializer = UserSerializer(instance=user)

    if user is None:
        raise AuthenticationFailed("User Not Found")

    if not user.check_password(password):
        raise AuthenticationFailed("Password Incorrect")

    token = Token.objects.get(user=user)

    response = {
        "user": serializer.data,
        "token": token.key
    }

    return Response(response, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def verify_token(request: Request):

    request_otp = request.data["otp"]
    user = request.user

    user_serializer = UserSerializer(instance=user)

    services.remove_old_otps()
    otp = OneTimePassword.objects.filter(email=user_serializer.data["email"], otp=request_otp, is_expired=False).first()

    if user is None:
        raise AuthenticationFailed("Invalid Authentication Token")
    otp_serializer = OTPSerializer(instance=otp)

    if otp is None:
        raise AuthenticationFailed("OTP does not exist")

    services.verify_otp(otp=otp, otp_serializer=otp_serializer, request_otp=request_otp)

    user.is_verified = True
    user.save()
    return Response(data=user_serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def generate_otp(request: Request):
    user = request.user
    pin = generate_pin()

    user_serializer = UserSerializer(instance=user)

    services.generate_otp(email=user_serializer.data["email"], pin=pin)

    return Response(data={
        "otp": pin
    }, status=status.HTTP_200_OK)

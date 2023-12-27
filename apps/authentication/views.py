from django.core.mail import send_mail

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from . import services
from .serializers import UserSerializer, OTPSerializer, PrinterSerializer
from rest_framework.authtoken.models import Token
from .models import User, OneTimePassword, Printer
from rest_framework import status
from .services import generate_pin
from rest_framework.exceptions import AuthenticationFailed
import datetime

from decouple import config


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

        token, created = Token.objects.get_or_create(user=user)

        data = {
            "user_id": user.id,
            "otp": pin,
            "token": token.key,
            "data": serializer.data
        }

        # TODO: Send mail to user containing the otp pin
        # send_mail(
        #     'Verify your Prompt Account!',
        #     f'Here is you One Time Password - {pin}',
        #     'bayodeiretomiwa@gmail.com',
        #     ['email'],
        #     fail_silently=False,
        # )

        return Response(data=data, status=status.HTTP_201_CREATED)

    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request: Request):
    email = request.data["email"]
    password = request.data["password"]

    user = User.objects.filter(email=email, is_verified=True).first()
    serializer = UserSerializer(instance=user)

    if user is None:
        raise AuthenticationFailed("User Not Found")

    if not user.check_password(password):
        raise AuthenticationFailed("Password Incorrect")

    token, created = Token.objects.get_or_create(user=user)

    response = {
        "user_id": user.id,
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

    response = {
        "id": user.id,
        "email": user.email,
        "message": "User has been verified"
    }
    return Response(data=response, status=status.HTTP_200_OK)


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


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_printer(request: Request):
    user = request.user
    if user.is_verified:

        printer = Printer.objects.create(user=user, id_user=user.id,
                                         description=request.data["description"], is_open=request.data["is_open"],
                                         phone_number=request.data["phone_number"], location=request.data["location"],
                                         offers_coloured=request.data["offers_coloured"],
                                         coloured_rate=request.data["coloured_rate"],
                                         uncoloured_rate=request.data["uncoloured_rate"]
                                         )

        user.is_printer = True
        user.save()

        printer_serializer = PrinterSerializer(instance=printer)
        return Response(data=printer_serializer.data, status=status.HTTP_201_CREATED)

    else:
        raise AuthenticationFailed("User is not verified by OTP")


@api_view(["PUT"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_rates(request: Request):
    return services.update_rates(request)

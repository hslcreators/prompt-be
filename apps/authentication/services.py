from random import randrange
import datetime

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework.response import Response

from apps.authentication.models import OneTimePassword, Printer
from apps.authentication.serializers import OTPSerializer


def generate_pin():
    return randrange(1000, 10000)


def verify_otp(otp, otp_serializer, request_otp):
    # This is for changing time to get the difference in time
    otp.dummy = "ct"
    otp.save()

    if (otp.expiry_date - otp.created) > datetime.timedelta(minutes=3):
        raise AuthenticationFailed("Token is Expired")

    otp_pin = otp_serializer.data["otp"]

    if int(otp_pin) != int(request_otp):
        raise AuthenticationFailed("OTP is is not the same")

    otp.is_expired = True
    otp.save()


def remove_old_otps():
    otps = OneTimePassword.objects.all()

    for otp in otps:
        otp.dummy = "ct"
        otp.save()
        if (otp.expiry_date - otp.created) > datetime.timedelta(minutes=3):
            otp.is_expired = True
            otp.save()


def generate_otp(email, pin):
    otp = OneTimePassword.objects.create(email=email, otp=pin)

    otp_serializer = OTPSerializer(data=otp)
    if otp_serializer.is_valid():
        otp_serializer.save()


def update_rates(request: Request):
    user = request.user
    printer = Printer.objects.get(user=user)

    coloured_rate = request.data["coloured_rate"]
    uncoloured_rate = request.data["uncoloured_rate"]

    if coloured_rate == "":
        coloured_rate = printer.coloured_rate
    if uncoloured_rate == "":
        uncoloured_rate = printer.uncoloured_rate

    printer.coloured_rate = int(coloured_rate)
    printer.uncoloured_rate = int(uncoloured_rate)

    printer.save()

    response = {
        "message": "Rates have been updates",
        "coloured_rate": printer.coloured_rate,
        "uncoloured_rate": printer.uncoloured_rate,
    }

    return Response(data=response, status=status.HTTP_200_OK)


def logout(request: Request):
    user = request.user

    Token.objects.get(user=user).delete()

    return Response({"message": "User has been successfully logged out"})

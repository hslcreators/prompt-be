from random import randrange
import datetime
from rest_framework.exceptions import AuthenticationFailed

from apps.authentication.models import OneTimePassword
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

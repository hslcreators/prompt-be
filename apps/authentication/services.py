from random import randrange
import datetime
from rest_framework.exceptions import AuthenticationFailed


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

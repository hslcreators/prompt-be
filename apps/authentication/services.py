from random import randrange
import datetime

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework.response import Response

from apps.authentication.models import OneTimePassword, Printer
from apps.authentication.serializers import OTPSerializer, PrinterSerializer


def generate_pin():
    return randrange(100000, 1000000)


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


def reset_password(request: Request):
    user = request.user
    new_password = request.data["password"]
    confirm_new_password = request.data["confirm_password"]

    if new_password == confirm_new_password:
        if not user.check_password(new_password):
            user.set_password(new_password)
            user.save()
            return Response({"data": "Password has been successfully reset"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Password cannot be the same as the old one"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Passwords do not Match"}, status=status.HTTP_400_BAD_REQUEST)


def logout(request: Request):
    user = request.user

    Token.objects.get(user=user).delete()

    return Response({"message": "User has been successfully logged out"})


def change_password(request: Request):
    user = request.user
    former_password = request.data["former_password"]
    new_password = request.data["new_password"]
    confirm_password = request.data["confirm_password"]

    if not user.check_password(former_password):
        return Response({"error": "Incorrect Password"}, status=status.HTTP_400_BAD_REQUEST)
    elif not new_password == confirm_password:
        return Response({"error": "Passwords do not Match"}, status=status.HTTP_400_BAD_REQUEST)
    elif user.check_password(new_password):
        return Response({"error": "Passwords cannot be the same as the former"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password has been successfully changed"}, status=status.HTTP_200_OK)
    
def find_printer_by_id(printer_id: int):
    printer = Printer.objects.get(id=printer_id)
    printer_serializer = PrinterSerializer(instance=printer)

    return Response(data=printer_serializer.data, status=status.HTTP_200_OK)

def find_printers_by_location(request: Request):
    location = request.data["location"]
    printers = Printer.objects.filter(location=location.upper())
    printers_serializer = PrinterSerializer(instance=printers, many=True)

    return Response(data=printers_serializer.data, status=status.HTTP_200_OK)

def find_all_printers():
    printers = Printer.objects.all()
    printer_serializer = PrinterSerializer(instance=printers, many=True)

    return Response(data=printer_serializer.data, status=status.HTTP_200_OK)

def find_all_locations():
    locations = []
    print("Hey")

    printers = Printer.objects.filter()

    for printer in printers:
        if printer.location not in locations:
            locations.append(printer.location)
        
    return Response(data=locations, status=status.HTTP_200_OK)

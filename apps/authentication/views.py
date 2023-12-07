from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import UserSerializer, OTPSerializer
from rest_framework.authtoken.models import Token
from .models import User, OneTimePassword
from rest_framework import status
from .services import generate_pin, is_otp_the_same


@api_view(["POST"])
def create_user(request: Request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data["username"])
        user.set_password(request.data["password"])

        pin = generate_pin()

        otp_data = {
            "otp": "{}".format(pin),
            "email": request.data["email"]
        }

        otp_serializer = OTPSerializer(data=otp_data)
        if otp_serializer.is_valid():
            otp_serializer.save()

        otp = OneTimePassword.objects.create(email=otp_data["email"], otp=otp_data["otp"], dummy="")

        token, created = Token.objects.get_or_create(user=user)

        data = {
            "otp": pin,
            "token": token.key,
            "data": serializer.data
        }

        # TODO: Send mail to user containing the otp pin

        user.save()
        otp.save()

        return Response(data=data, status=status.HTTP_201_CREATED)

    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

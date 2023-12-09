from rest_framework import serializers
from .models import User, OneTimePassword


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ["username", "first_name", "last_name", "email", "date_joined", "profile_picture", "is_printer",
                  "is_verified", "account_number", "bank_name", "account_name"]


class OTPSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = OneTimePassword
        fields = ["otp", "expiry_date", "email", "created", "dummy", "is_expired"]
from rest_framework import serializers
from .models import User, OneTimePassword, Printer


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ["username", "first_name", "last_name", "email", "date_joined", "profile_picture", "is_printer",
                  "is_verified", "account_number", "bank_name", "account_name"]


class OTPSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = OneTimePassword
        fields = ["otp", "expiry_date", "email", "created", "dummy", "is_expired"]


class PrinterSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Printer
        fields = ["id", "user", "id_user", "description", "is_open", "phone_number", "location", "average_rating",
                  "offers_coloured", "uncoloured_rate", "coloured_rate"]

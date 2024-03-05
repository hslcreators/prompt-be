from rest_framework import serializers

class SignUpRequest(serializers.Serializer):
    email = serializers.EmailField()
    profile_picture = serializers.ImageField()
    is_printer = serializers.BooleanField()
    is_verified = serializers.BooleanField()
    account_number = serializers.IntegerField()
    bank_name = serializers.CharField()
    account_name = serializers.CharField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    date_joined = serializers.DateTimeField()
    is_active = serializers.BooleanField()
    is_staff = serializers.BooleanField()
    password = serializers.CharField()

class LoginRequest(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class VerifyTokenRequest(serializers.Serializer):
    otp = serializers.IntegerField()

class CreatePrinterRequest(serializers.Serializer):
    description = serializers.CharField()
    is_open = serializers.BooleanField()
    phone_numbers = serializers.CharField()
    location = serializers.CharField()
    offers_coloured = serializers.BooleanField()
    coloured_rate = serializers.IntegerField()
    uncoloured_rate = serializers.IntegerField()

class UpdateRatesRequest(serializers.Serializer):
    coloured_rate = serializers.CharField()
    uncoloured_rate = serializers.CharField()

class ResetPasswordRequest(serializers.Serializer):
    password = serializers.CharField()
    confirm_password = serializers.CharField()

class ChangePasswordRequest(serializers.Serializer):
    former_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

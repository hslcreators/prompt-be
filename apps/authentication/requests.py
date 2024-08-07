from rest_framework import serializers

class SignUpRequest(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()

class LoginRequest(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class VerifyTokenRequest(serializers.Serializer):
    otp = serializers.IntegerField()

class CreatePrinterRequest(serializers.Serializer):
    description = serializers.CharField()
    print_service_name = serializers.CharField(max_length=225)
    phone_number = serializers.CharField()
    location = serializers.CharField()
    offers_coloured = serializers.BooleanField()
    coloured_rate = serializers.IntegerField()
    uncoloured_rate = serializers.IntegerField()
    account_number = serializers.DecimalField(decimal_places=0, max_digits=20)
    bank_name = serializers.CharField()
    account_name = serializers.CharField()

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

class GetPrinterByLocationRequest(serializers.Serializer):
    location = serializers.CharField()

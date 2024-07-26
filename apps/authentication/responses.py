from rest_framework import serializers

class SignUpResponse(serializers.Serializer):
    user_id = serializers.IntegerField()
    otp = serializers.IntegerField()
    token = serializers.CharField()
    is_verified = serializers.BooleanField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class LoginResponse(serializers.Serializer):
    user_id = serializers.CharField()
    token = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

class VerifyTokenResponse(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    message = serializers.CharField()

class GenerateTokenResponse(serializers.Serializer):
    otp = serializers.IntegerField()

class UpdateRatesResponse(serializers.Serializer):
    message = serializers.CharField()
    coloured_rate = serializers.CharField()
    uncoloured_rate = serializers.CharField()

class ResetPasswordResponse(serializers.Serializer):
    data = serializers.CharField()

class LogoutResponse(serializers.Serializer):
    message = serializers.CharField()

class ChangePasswordResponse(serializers.Serializer):
    message = serializers.CharField()

class FindAllLocationsResponse(serializers.Serializer):
    message = serializers.CharField(default="Ignore the JSON this endpoint returns a list of locations")

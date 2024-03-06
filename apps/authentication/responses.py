from rest_framework import serializers

class SignUpResponse(serializers.Serializer):
    user_id = serializers.IntegerField()
    otp = serializers.IntegerField()
    token = serializers.CharField()
    username = serializers.CharField()

class LoginResponse(serializers.Serializer):
    user_id = serializers.CharField()
    token = serializers.CharField()

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

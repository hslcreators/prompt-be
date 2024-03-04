from rest_framework import serializers

class SignUpResponse(serializers.Serializer):
    user_id = serializers.IntegerField()
    otp = serializers.IntegerField()
    token = serializers.CharField()
    username = serializers.CharField()

class LoginResponse(serializers.Serializer):
    user_id = serializers.CharField()
    token = serializers.CharField()

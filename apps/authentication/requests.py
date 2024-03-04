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

from rest_framework import serializers

class CreateOrderRequest(serializers.Serializer):
    no_of_copies = serializers.IntegerField()
    pages = serializers.IntegerField()
    coloured = serializers.BooleanField()
    document = serializers.FileField()
    description = serializers.CharField()
    time_expected = serializers.TimeField()
    pay_on_collection = serializers.BooleanField()

class UpdateStatusRequest(serializers.Serializer):
    is_complete = serializers.BooleanField()    

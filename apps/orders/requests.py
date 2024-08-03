from rest_framework import serializers

class CreateOrderRequest(serializers.Serializer):
    printer_id = serializers.IntegerField()
    no_of_copies = serializers.IntegerField()
    pages = serializers.IntegerField()
    coloured = serializers.BooleanField()
    document = serializers.CharField(default="You actually need to add a file not a characters into this field")
    description = serializers.CharField()
    time_expected = serializers.TimeField()

class UpdateStatusRequest(serializers.Serializer):
    is_complete = serializers.BooleanField()    

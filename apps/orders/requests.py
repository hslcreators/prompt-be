from rest_framework import serializers

class CreateOrderRequest(serializers.Serializer):
    printer_id = serializers.IntegerField()
    no_of_copies = serializers.IntegerField()
    pages = serializers.IntegerField()
    coloured = serializers.BooleanField()
    documents = serializers.ListField(default="You need to pass in a list of files")
    description = serializers.CharField()
    time_expected = serializers.TimeField()

class UpdateStatusRequest(serializers.Serializer):
    is_complete = serializers.BooleanField()    

from rest_framework import serializers

class OrderScheduleResponse(serializers.Serializer):
    order_id = serializers.UUIDField()
    pickup_time = serializers.TimeField()
    is_complete = serializers.BooleanField()
    paid = serializers.BooleanField()

class UpdateStatusResponse(serializers.Serializer):
    data = serializers.CharField()

class OrderResponse(serializers.Serializer):
    id = serializers.UUIDField()
    user = serializers.IntegerField()
    printer = serializers.IntegerField()
    no_of_copies = serializers.IntegerField()
    pages = serializers.IntegerField()
    coloured = serializers.BooleanField()
    order_time = serializers.DateTimeField()
    is_complete = serializers.BooleanField()
    paid = serializers.BooleanField()
    charge = serializers.IntegerField()
    documents = serializers.ListField(
        child=serializers.CharField(default="These are actually a list of javascript objects in the form {id: intId, name:'filename'}")
    )
    description = serializers.CharField()
    time_expected = serializers.TimeField()
    customer_name = serializers.CharField()
    vendor_name = serializers.CharField()

class OrderDocumentResponse(serializers.Serializer):
    id = serializers.IntegerField()
    document_name = serializers.CharField()
    document = serializers.CharField()

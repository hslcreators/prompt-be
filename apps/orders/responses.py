from rest_framework import serializers

class OrderScheduleResponse(serializers.Serializer):
    order_id = serializers.UUIDField()
    pickup_time = serializers.TimeField()
    is_complete = serializers.BooleanField()
    paid = serializers.BooleanField()

class UpdateStatusResponse(serializers.Serializer):
    data = serializers.CharField()

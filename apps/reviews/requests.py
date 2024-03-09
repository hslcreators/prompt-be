from rest_framework import serializers

class CreateReviewRequest(serializers.Serializer):
    printer_id = serializers.IntegerField()
    rating = serializers.IntegerField()
    comment = serializers.CharField()

class EditReviewRequest(serializers.Serializer):
    rating = serializers.IntegerField()
    comment = serializers.CharField()

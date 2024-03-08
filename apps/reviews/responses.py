from rest_framework import serializers

class DeleteReviewResponse(serializers.Serializer):
    message = serializers.CharField()
    value = serializers.BooleanField()

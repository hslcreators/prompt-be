from rest_framework import serializers

from apps.orders.models import Order, OrderDocument


class OrderSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Order
        fields = ["id", "user", "printer", "no_of_copies", "pages", "description", "order_time", "time_expected", "is_complete", "paid", "coloured", "charge"]

class OrderDocumentSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = OrderDocument
        fields = ["document"]

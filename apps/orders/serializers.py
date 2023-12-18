from rest_framework import serializers

from apps.orders.models import Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Order
        fields = ["id", "user", "printer", "document", "no_of_copies", "pages", "description", "order_time", "time_expected", "is_complete", "pay_on_collection", "paid"]
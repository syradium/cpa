from rest_framework import serializers
from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['created_on', 'order_id', 'domain', 'price', 'data', 'pk']

from rest_framework import serializers
from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['created_on', 'order_id', 'domain', 'price', 'data', 'pk', 'utm_source', 'utm_campaign', 'utm_content']


class OrderSerializerPostback(OrderSerializer):
    utm1 = serializers.CharField(default='', allow_blank=True, source='utm_source', write_only=True)
    utm2 = serializers.CharField(default='', allow_blank=True, source='utm_campaign', write_only=True)
    utm3 = serializers.CharField(default='', allow_blank=True, source='utm_content', write_only=True)

    class Meta:
        model = Order
        fields = ['created_on', 'order_id', 'domain', 'price', 'data', 'pk', 'utm1', 'utm2', 'utm3']

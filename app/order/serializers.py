from rest_framework import serializers

from .models import Order, OrderItem
from art.serializers import *

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "art", "frame", "passepartout", "quantity", "unit_price"]
        read_only_fields = fields


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    discount_code = serializers.SlugRelatedField(slug_field="code", read_only=True)    
    
    class Meta:
        model = Order
        fields = [
            "id", "address", "status", "destination", "discount_code",
            "items_price", "shipping_price", "discount_amount", "total_price",
            "items", "created_at", "updated_at", "paid_at", "cancelled_at",
        ]
        read_only_fields = fields

class OrderCreateSerializer(serializers.Serializer):
    address = serializers.IntegerField()
    destination = serializers.ChoiceField(choices=Order.Destination.choices)
    discount_code = serializers.CharField(required=False, allow_blank=True)


class DiscountCodeCheckSerializer(serializers.Serializer):
    code = serializers.CharField()
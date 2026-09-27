from rest_framework import serializers

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "art", "frame", "passepartout", "quantity", "unit_price"]
        read_only_fields = ["id", "unit_price"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["items","total_price", "created_at", "updated_at"]
        read_only_fields = ["total_price", "created_at", "updated_at"]
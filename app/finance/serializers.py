from rest_framework import serializers

from .models import PriceBase, DiscountCode

class PriceBaseSerializer(serializers.Serializer):
    canvas = serializers.IntegerField(required=False, min_value=0)
    fiber = serializers.IntegerField(required=False, min_value=0)
    glue = serializers.IntegerField(required=False, min_value=0)
    initial_print = serializers.IntegerField(required=False, min_value=0)
    passepartout = serializers.IntegerField(required=False, min_value=0)
    labor = serializers.IntegerField(required=False, min_value=0)
    shipping_tehran = serializers.IntegerField(required=False, min_value=0)
    shipping_other = serializers.IntegerField(required=False, min_value=0)

class DiscountCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DiscountCode
        fields = ['id', 'type', 'title', 'code', 'expires_at', 'quantity', 'used_count', 'amount', 'created_at', 'updated_at']

        read_only_fields = [
            'id', 'used_count', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        discount_type = attrs.get('type', getattr(self.instance, 'type', None))
        amount = attrs.get('amount', getattr(self.instance, 'amount', None))
        
        if discount_type == DiscountCode.DiscountType.PERCENTAGE:
            if amount > 100:
                raise serializers.ValidationError({'amount': 'مقدار درصد نمی تواند بیشتر از 100 باشد'})

        return attrs
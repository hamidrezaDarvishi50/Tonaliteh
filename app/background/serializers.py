from .models import BackgroundImage
from rest_framework import serializers

class BackgroundImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackgroundImage
        fields = ['id', 'image', 'created_at']
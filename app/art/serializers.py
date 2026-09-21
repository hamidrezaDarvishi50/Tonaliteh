from rest_framework import serializers

from .models import Art, Artist, Category

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name', 'slug', 'bio', 'image', 'created_at']
        read_only_fields = ['slug']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image']
        read_only_fields = ['slug']

class ArtSerializer(serializers.ModelSerializer):
    
    artist = serializers.SlugRelatedField(slug_field='name', queryset=Artist.objects.all())
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    
    class Meta:
        model = Art
        fields = ['id', 'artist', 'category', 'name', 'slug', 'image', 'width', 'height', 'created_at', 'updated_at']
        read_only_fields = ['slug']


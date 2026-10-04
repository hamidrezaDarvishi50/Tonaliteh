from rest_framework import serializers

from .models import *

class ArtSerializer(serializers.ModelSerializer):
    artist = serializers.SlugRelatedField(slug_field='name', queryset=Artist.objects.all())
    category = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Category.objects.all())
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    
    class Meta:
        model = Art
        fields = ['id', 'name', 'slug', 'persian_name',
                'artist', 'category', 'tags',
                'image', 'voice', 'second_voice',
                'width', 'height', 'released_year',
                'created_at', 'updated_at']
        read_only_fields = ['slug']

class ArtDetailSerializer(serializers.ModelSerializer):
    artist = serializers.SlugRelatedField(slug_field='name', queryset=Artist.objects.all())
    
    class Meta:
        model = Art
        fields = ['id', 'artist', 'name', 'slug', 'image', 'released_year']
        read_only_fields = ['slug']

class ArtDetailSerializer2(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Art
        fields = ['id', 'category', 'name', 'slug', 'image', 'released_year']
        read_only_fields = ['slug']

class ArtistSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Artist
        fields = ['id', 'name', 'slug', 'bio', 'image', 'created_at']
        read_only_fields = ['slug']
        
class ArtistِDetailSerializer(serializers.ModelSerializer):
    arts = ArtDetailSerializer2(read_only=True, many=True)
    
    class Meta:
        model = Artist
        fields = ['id', 'name', 'slug', 'bio', 'image', 'created_at','arts']
        read_only_fields = ['slug']
        

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image']
        read_only_fields = ['slug']

class CategoryDetailSerializer(serializers.ModelSerializer):
    arts = ArtDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'arts']
        read_only_fields = ['slug']



class FrameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Frame
        fields = ['id', 'title', 'description', 'square_image', 'corner_image', 'horizontal_image', 'vertical_image', 'order', 'width', 'price']

class PassepartoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passepartout
        fields = ['id', 'distance']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "type", "name"]


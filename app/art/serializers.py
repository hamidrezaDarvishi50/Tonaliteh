from rest_framework import serializers

from .models import Art, Artist, Category

class ArtSerializer(serializers.ModelSerializer):
    artist = serializers.SlugRelatedField(slug_field='name', queryset=Artist.objects.all())
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    
    class Meta:
        model = Art
        fields = ['id', 'artist', 'category', 'name', 'slug', 'image', 'width', 'height', 'released_year', 'created_at', 'updated_at']
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


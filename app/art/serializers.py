from rest_framework import serializers

from .models import *

ALLOWED_AUDIO_TYPES = {
    "audio/mpeg",
    "audio/wav",
    "audio/x-wav",
    "audio/ogg",
    "audio/mp4",
    "audio/aac",
}

def validate_audio_file(file):
    if file.content_type not in ALLOWED_AUDIO_TYPES:
        raise serializers.ValidationError(
            "Only audio files are allowed."
        )

    return file

class ArtSerializer(serializers.ModelSerializer):
    artist = serializers.SlugRelatedField(slug_field='name', queryset=Artist.objects.all())
    category = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Category.objects.all())
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    
    voice = serializers.FileField(required=False, allow_null=True, validators=[validate_audio_file])
    second_voice = serializers.FileField(required=False, allow_null=True, validators=[validate_audio_file])
    
    class Meta:
        model = Art
        fields = ['id', 'name', 'slug', 'persian_name', 'title', 'description',
                'artist', 'category', 'tags',
                'image', 'voice', 'second_voice',
                'width', 'height', 'released_year',
                'created_at', 'updated_at']

class ArtDetailSerializer(serializers.ModelSerializer):
    artist = serializers.SlugRelatedField(slug_field='name', queryset=Artist.objects.all())
    
    class Meta:
        model = Art
        fields = ['id', 'artist', 'name', 'slug', 'image', 'released_year']

class ArtDetailSerializer2(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Art
        fields = ['id', 'category', 'name', 'slug', 'image', 'released_year']

class ArtistSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Artist
        fields = ['id', 'name', 'persian_name',
                'title', 'description' 'slug', 'order',
                'image', 'banner_image',
                'banner1', 'banner2', 'head1', 'head2',
                'created_at', 'updated_at']
        
class ArtistِDetailSerializer(serializers.ModelSerializer):
    arts = ArtDetailSerializer2(read_only=True, many=True)
    
    class Meta:
        model = Artist
        fields = ['id', 'name', 'slug', 'bio', 'image', 'created_at','arts']
        

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'persian_name',
                'slug', 'description',
                'image']

class CategoryDetailSerializer(serializers.ModelSerializer):
    arts = ArtDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'persian_name',
                'slug', 'description', 'image', 'arts']


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


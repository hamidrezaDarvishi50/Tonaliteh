from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Comment

ALLOWED_MODELS = ['art', 'artist', 'category', 'blog']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    content_type = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.filter(model__in=ALLOWED_MODELS),)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content_type', 'object_id', 'text', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate(self, attrs):
        content_type = attrs.get('content_type')
        object_id = attrs.get('object_id')
        model_class = content_type.model_class()
        if not model_class.objects.filter(pk=object_id).exists():
            raise serializers.ValidationError({"object_id": "آبجکت مورد نظر پیدا نشد."})
        return attrs
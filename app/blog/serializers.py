from rest_framework import serializers
import json
from .models import *

class BlogFAQSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogFAQ
        fields = ['id', 'question', 'answer']    

class BlogSerializer(serializers.ModelSerializer):
    
    arts = serializers.PrimaryKeyRelatedField(many=True, queryset=Art.objects.all())
    faqs = BlogFAQSerializer(many=True)

    class Meta:
        model= Blog
        fields = ['id', 'title', 'author_name', 'author_description',
                'table_of_contents', 'description', 'short_description','final_description',
                'main_image', 'arts', 'faqs',
                'title_seo','slug', 'meta_description',
                'created_at', 'updated_at']
        
        read_only_fields = ["id", "created_at", "updated_at"]
        
    # def to_internal_value(self, data):
    #     data = data.copy()

    #     if isinstance(data.get("faqs"), str):
    #         data["faqs"] = json.loads(data["faqs"])

    #     return super().to_internal_value(data)
        
    def create(self, validated_data):
        faqs = validated_data.pop('faqs', [])
        arts_data = validated_data.pop("arts", [])
        blog = Blog.objects.create(**validated_data)
        blog.arts.set(arts_data)
        
        for faq in faqs:
            BlogFAQ.objects.create(blog=blog, **faq)

        return blog
from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.contenttypes.models import ContentType

from .models import Comment
from .serializers import CommentSerializer


class CommentListView(APIView):
    def get(self, request):
        model_name = request.query_params.get('content_type')
        object_id = request.query_params.get('object_id')

        content_type = get_object_or_404(ContentType, model=model_name)
        comments = Comment.objects.filter(
            content_type=content_type, object_id=object_id
        ).select_related('user')

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
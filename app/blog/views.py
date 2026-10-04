from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *
from accounts.authentication import user_authenticate


class BlogView(APIView):
    
    def get(self, request:Request):
        blogs = Blog.objects.prefetch_related("faqs", "arts")
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request:Request):
        
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail":"admin access required"}, status.HTTP_401_UNAUTHORIZED)
        
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "A new blog is created"}, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            
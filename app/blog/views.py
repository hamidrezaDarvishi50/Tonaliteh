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
        
    

class BlogDetailView(APIView):
    
    def get_object(self, slug):
        try:
            return Blog.objects.prefetch_related("faqs", "arts").get(slug=slug)
        except Blog.DoesNotExist:
            return None
    
    def get(self, request: Request, slug):
        blog = self.get_object(slug)
        if blog is None:
            return Response({"detail": "بلاگ پیدا نشد"}, status.HTTP_404_NOT_FOUND)

        serializer = BlogSerializer(blog)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def put(self, request: Request, slug):
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)

        blog = self.get_object(slug)
        if blog is None:
            return Response({"detail": "بلاگ پیدا نشد"}, status.HTTP_404_NOT_FOUND)

        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "بلاگ به روز شد"}, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request: Request, slug):
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)

        blog = self.get_object(slug)
        if blog is None:
            return Response({"detail": "بلاگ پیدا نشد"}, status.HTTP_404_NOT_FOUND)

        blog.delete()
        return Response({"detail": "بلاگ با موفقیت حذف شد"}, status.HTTP_200_OK)
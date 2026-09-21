from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .models import Art, Artist, Category
from .serializers import ArtistSerializer, ArtSerializer, CategorySerializer
from accounts.authentication import user_authenticate

class ArtistListView(APIView):
    def get(self, request: Request):
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request: Request):
        
        user = user_authenticate(request)

        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status=status.HTTP_403_FORBIDDEN)
            
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "A new artist is created"}, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class ArtistDetailView(APIView):
    
    def get_object(self, slug):
        try:
            return Artist.objects.get(slug=slug)
        except Artist.DoesNotExist:
            return None
    
    def get(self, request: Request, slug):
        artist = self.get_object(slug)
        serializer = ArtistSerializer(artist)
        if artist is None:
            return Response({"detail": "Artist not found."}, status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def put(self, request: Request, slug):
        user = user_authenticate(request)
        
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status=status.HTTP_403_FORBIDDEN)

        artist = self.get_object(slug)
        if artist is None:
            return Response({"detail": "Artist not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ArtistSerializer(Artist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Artist is successfully updated"}, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request: Request, slug):
        
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status=status.HTTP_403_FORBIDDEN)
        
        artist = self.get_object(slug)
        if artist is None:
            return Response({"detail" : "Artist not found."}, status=status.HTTP_404_NOT_FOUND)

        artist.delete()
        return Response({"detail": "Artist deleted successfully."}, status.HTTP_200_OK)


class CategoryListView(APIView):
    def get(self, request: Request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request: Request):
        user = user_authenticate(request)

        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)
            
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "A new category is created"}, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class CategoryDetailView(APIView):
    
    def get_object(self, slug):
        try:
            return Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return None
        
    def get(self, request: Request, slug):
        category = self.get_object(slug)        
        if category is None:
            return Response({"detail": "Category not found."}, status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category)
        return Response(serializer.data, status.HTTP_200_OK)
        
    def put(self, request: Request, slug):
        
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status=status.HTTP_403_FORBIDDEN)
        
        category = self.get_object(slug)
        if category is None:
            return Response({"detail" : "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Category is successfully updated"}, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request: Request, slug):
        
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status=status.HTTP_403_FORBIDDEN)
        
        category = self.get_object(slug)
        if category is None:
            return Response({"detail" : "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        
        category.delete()
        return Response({"detail": "Category deleted successfully."}, status.HTTP_200_OK)


class ArtListView(APIView):
    def get(self, request: Request):
        arts = Art.objects.all()
        serializer = ArtSerializer(arts, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
            
    def post(self, request: Request):
        user = user_authenticate(request)
        
        if not user.is_staff:
            return Response({"detail": "Admin access required"}, status.HTTP_403_FORBIDDEN)

        serializer = ArtSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "A new category is created"}, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class ArtDetailView(APIView):
    def get(request: Request):
        pass
    
    def put(request: Request):
        pass
    
    def delete(request: Request):
        pass
    
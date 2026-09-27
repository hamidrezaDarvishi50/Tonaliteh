from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *
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
        if artist is None:
            return Response({"detail": "Artist not found."}, status.HTTP_404_NOT_FOUND)
        
        serializer = ArtistِDetailSerializer(artist)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def put(self, request: Request, slug):
        user = user_authenticate(request)
        
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status=status.HTTP_403_FORBIDDEN)

        artist = self.get_object(slug)
        if artist is None:
            return Response({"detail": "Artist not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ArtistSerializer(artist, data=request.data)
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

        serializer = CategoryDetailSerializer(category)
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
            return Response({"detail": "A new art is created"}, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class ArtDetailView(APIView):
    
    def get_object(self, slug):
        try:
            return Art.objects.get(slug=slug)
        except Art.DoesNotExist:
            return None
    
    def get(self, request: Request, slug):
        art = self.get_object(slug)
        
        if art is None:
            return Response({"detail":"Art not found"}, status.HTTP_404_NOT_FOUND)

        serializer = ArtSerializer(art)
        return Response(serializer.data, status.HTTP_200_OK)
        
    def put(self, request: Request, slug):
        
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail":"Admin access required"}, status.HTTP_403_FORBIDDEN)

        art = self.get_object(slug)
        if art is None:
            return Response({"detail":"Art not found"}, status.HTTP_404_NOT_FOUND)

        serializer = ArtSerializer(art, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail":"Art is successfully updated"}, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, slug):
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail":"Admin access required"}, status.HTTP_403_FORBIDDEN)

        art = self.get_object(slug)
        if art is None:
            return Response({"detail":"Art not found"}, status.HTTP_404_NOT_FOUND)

        art.delete()
        return Response({"detail":"Art deleted successfully."}, status.HTTP_200_OK)

    
class FrameListView(APIView):

    def get(self, request: Request):
        
        frames = Frame.objects.all().order_by('order')
        serializer = FrameSerializer(frames, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request):
        
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)

        serializer = FrameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail":"قاب با موفقیت اضافه شد"}, status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class FrameDetailView(APIView):

    def get_object(self, pk):
        try:
            return Frame.objects.get(pk=pk)
        except Frame.DoesNotExist:
            return None
    
    def get(self, request:Request, pk):
        frame = self.get_object(pk)
        if frame is None:
            return Response({"detail": "قاب پیدا نشد"}, status.HTTP_404_NOT_FOUND)

        serializer = FrameSerializer(frame)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request: Request, pk):
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)

        frame = self.get_object(pk)
        if frame is None:
            return Response({"detail": "قاب پیدا نشد"}, status.HTTP_404_NOT_FOUND)

        serializer = FrameSerializer(frame, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "قاب با موفقیت ویرایش شد"}, status.HTTP_200_OK)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk):
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)

        frame = self.get_object(pk)
        if frame is None:
            return Response({"detail": "قاب پیدا نشد"}, status.HTTP_404_NOT_FOUND)

        frame.delete()

        return Response({"detail": "قاب با موفقیت حذف شد"}, status.HTTP_200_OK)


class PassepartoutListView(APIView):

    def get(self, request: Request):
        passepartouts = Passepartout.objects.all().order_by('distance')
        serializer = PassepartoutSerializer(passepartouts, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request):
        
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)

        serializer = PassepartoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"datail":"پاسپارتو با موفقیت اضافه شد"}, status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class PassepartoutDetailView(APIView):

    def get_object(self, pk):
        try:
            return Passepartout.objects.get(pk=pk)
        except Passepartout.DoesNotExist:
            return None

    def get(self, request: Request, pk):
        passepartout = Passepartout.objects.get(pk=pk)
        if passepartout is None:
            return Response({"detail": "پاسپارتو پیدا نشد"}, status.HTTP_404_NOT_FOUND)

        serializer = PassepartoutSerializer(passepartout)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request: Request, pk):
        
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)

        passepartout = Passepartout.objects.get(pk=pk)
        if passepartout is None:
            return Response({"detail": "پاسپارتو پیدا نشد"}, status.HTTP_404_NOT_FOUND)

        serializer = PassepartoutSerializer(passepartout, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk):
        
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)

        passepartout = Passepartout.objects.get(pk=pk)
        if passepartout is None:
            return Response({"detail": "پاسپارتو پیدا نشد"}, status.HTTP_404_NOT_FOUND)

        passepartout.delete()
        return Response({"detail": "پاسپارتو با موفقیت حذف شد"}, status.HTTP_200_OK)
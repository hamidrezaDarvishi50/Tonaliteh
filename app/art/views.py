from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *
from accounts.authentication import user_authenticate

from .filters import *
from django.db.models import Q

from drf_spectacular.utils import extend_schema

class ArtistListView(APIView):
    
    @extend_schema(
        responses={200: ArtistSerializer(many=True),})
    def get(self, request: Request):
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    @extend_schema(
        request=ArtistSerializer,
        responses={
            201: {"type": "object"},
            400: {"type": "object"},
            401: {"type": "object"},
            403: {"type": "object"},})
    def post(self, request: Request):
        
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)
            
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
    
    @extend_schema(
        responses={
            200: ArtistِDetailSerializer,
            404: {"type": "object"},})
    def get(self, request: Request, slug):
        artist = self.get_object(slug)
        if artist is None:
            return Response({"detail": "Artist not found."}, status.HTTP_404_NOT_FOUND)
        
        serializer = ArtistِDetailSerializer(artist)
        return Response(serializer.data, status.HTTP_200_OK)
    
    @extend_schema(
        request=ArtistSerializer,
        responses={
            200: {"type": "object"},
            400: {"type": "object"},
            401: {"type": "object"},
            403: {"type": "object"},
            404: {"type": "object"},})
    def put(self, request: Request, slug):
        user = user_authenticate(request)
        
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)

        artist = self.get_object(slug)
        if artist is None:
            return Response({"detail": "Artist not found."}, status.HTTP_404_NOT_FOUND)
        
        serializer = ArtistSerializer(artist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Artist is successfully updated"}, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        responses={
            200: {"type": "object"},
            401: {"type": "object"},
            403: {"type": "object"},
            404: {"type": "object"},})
    def delete(self, request: Request, slug):
        
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)
        
        artist = self.get_object(slug)
        if artist is None:
            return Response({"detail" : "Artist not found."}, status.HTTP_404_NOT_FOUND)

        artist.delete()
        return Response({"detail": "Artist deleted successfully."}, status.HTTP_200_OK)


class CategoryListView(APIView):
    @extend_schema(responses={200: CategorySerializer(many=True),})
    def get(self, request: Request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    @extend_schema(
        request=CategorySerializer,
        responses={
            201: {"type": "object"},
            400: {"type": "object"},
            401: {"type": "object"},
            403: {"type": "object"},})
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
    
    @extend_schema(
        responses={
            200: CategoryDetailSerializer,
            404: {"type": "object"},})
    def get(self, request: Request, slug):
        category = self.get_object(slug)        
        if category is None:
            return Response({"detail": "Category not found."}, status.HTTP_404_NOT_FOUND)

        serializer = CategoryDetailSerializer(category)
        return Response(serializer.data, status.HTTP_200_OK)

    @extend_schema(
        request=CategorySerializer,
        responses={
            200: {"type": "object"},
            400: {"type": "object"},
            401: {"type": "object"},
            403: {"type": "object"},
            404: {"type": "object"},})
    def put(self, request: Request, slug):
        
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)
        
        category = self.get_object(slug)
        if category is None:
            return Response({"detail" : "Category not found."}, status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Category is successfully updated"}, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={
            200: {"type": "object"},
            401: {"type": "object"},
            403: {"type": "object"},
            404: {"type": "object"},})
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
    
    @extend_schema(responses={200: ArtSerializer(many=True),})
    def get(self, request: Request):
        arts = search_arts(request.query_params)
        arts = sort_arts(arts, request.query_params.get("sort"))
        serializer = ArtSerializer(arts, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    @extend_schema(
        request=ArtSerializer,
        responses={
            201: {"type": "object"},
            400: {"type": "object"},
            401: {"type": "object"},
            403: {"type": "object"},})
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
    
    @extend_schema(
        responses={
            200: ArtSerializer,
            404: {"type": "object"},})
    def get(self, request: Request, slug):
        art = self.get_object(slug)
        
        if art is None:
            return Response({"detail":"Art not found"}, status.HTTP_404_NOT_FOUND)

        serializer = ArtSerializer(art)
        return Response(serializer.data, status.HTTP_200_OK)
        
    @extend_schema(
        request=ArtSerializer,
        responses={
            200: {"type": "object"},
            400: {"type": "object"},
            401: {"type": "object"},
            403: {"type": "object"},
            404: {"type": "object"},})
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

    @extend_schema(
        responses={
            200: {"type": "object"},
            401: {"type": "object"},
            403: {"type": "object"},
            404: {"type": "object"},})
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

    @extend_schema(responses={200: FrameSerializer(many=True),})
    def get(self, request: Request):
        
        frames = Frame.objects.all().order_by('order')
        serializer = FrameSerializer(frames, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @extend_schema(
        request=FrameSerializer,
        responses={
            201: {"type": "object"},
            400: {"type": "object"},
            401: {"type": "object"},
            403: {"type": "object"},})
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
    
    @extend_schema(
        responses={
            200: FrameSerializer,
            404: {"type": "object"},})
    def get(self, request:Request, pk):
        frame = self.get_object(pk)
        if frame is None:
            return Response({"detail": "قاب پیدا نشد"}, status.HTTP_404_NOT_FOUND)

        serializer = FrameSerializer(frame)
        return Response(serializer.data, status.HTTP_200_OK)

    @extend_schema(
        request=FrameSerializer,
        responses={
            200: {"type": "object"},
            400: {"type": "object"},
            401: {"type": "object"},
            403: {"type": "object"},
            404: {"type": "object"},})
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

    @extend_schema(
        responses={
            200: {"type": "object"},
            401: {"type": "object"},
            403: {"type": "object"},
            404: {"type": "object"},})
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

    @extend_schema(responses={200: PassepartoutSerializer(many=True),})
    def get(self, request: Request):
        passepartouts = Passepartout.objects.all().order_by('distance')
        serializer = PassepartoutSerializer(passepartouts, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @extend_schema(
        request=PassepartoutSerializer,
        responses={
            201: {"type": "object"},
            400: {"type": "object"},
            401: {"type": "object"},
            403: {"type": "object"},})
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

    @extend_schema(
        responses={
            200: PassepartoutSerializer,
            404: {"type": "object"},})
    def get(self, request: Request, pk):
        passepartout = self.get_object(pk=pk)
        if passepartout is None:
            return Response({"detail": "پاسپارتو پیدا نشد"}, status.HTTP_404_NOT_FOUND)

        serializer = PassepartoutSerializer(passepartout)
        return Response(serializer.data, status.HTTP_200_OK)

    @extend_schema(
        request=PassepartoutSerializer,
        responses={
            200: PassepartoutSerializer,
            400: {"type": "object"},
            401: {"type": "object"},
            403: {"type": "object"},
            404: {"type": "object"},})
    def put(self, request: Request, pk):
        
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)

        passepartout = self.get_object(pk=pk)
        if passepartout is None:
            return Response({"detail": "پاسپارتو پیدا نشد"}, status.HTTP_404_NOT_FOUND)

        serializer = PassepartoutSerializer(passepartout, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={
            200: {"type": "object"},
            401: {"type": "object"},
            403: {"type": "object"},
            404: {"type": "object"},})
    def delete(self, request: Request, pk):
        
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)

        passepartout = Passepartout.objects.get(pk=pk)
        if passepartout is None:
            return Response({"detail": "پاسپارتو پیدا نشد"}, status.HTTP_404_NOT_FOUND)

        passepartout.delete()
        return Response({"detail": "پاسپارتو با موفقیت حذف شد"}, status.HTTP_200_OK)

class TagListView(APIView):

    @extend_schema(responses={200: TagSerializer(many=True),})
    def get(self, request: Request):
        tags = Tag.objects.all()

        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @extend_schema(
        request=TagSerializer,
        responses={
            201: TagSerializer,
            400: {"type": "object"},
            401: {"type": "object"},
            403: {"type": "object"},})
    def post(self, request: Request):
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)

        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class TagDetailView(APIView):

    def get_object(self, pk):
        try:
            return Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return None

    @extend_schema(
        request=TagSerializer,
        responses={
            200: TagSerializer,
            400: {"type": "object"},
            401: {"type": "object"},
            403: {"type": "object"},
            404: {"type": "object"},})
    def put(self, request: Request, pk):
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)

        tag = self.get_object(pk)
        if tag is None:
            return Response({"detail": "تگ پیدا نشد"}, status.HTTP_404_NOT_FOUND)

        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={
            200: {"type": "object"},
            401: {"type": "object"},
            403: {"type": "object"},
            404: {"type": "object"},})
    def delete(self, request: Request, pk):
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)

        tag = self.get_object(pk)
        if tag is None:
            return Response({"detail": "تگ پیدا نشد"}, status.HTTP_404_NOT_FOUND)

        tag.delete()
        return Response({"detail": "تگ با موفقیت حذف شد"}, status.HTTP_200_OK)


# search box
class SearchView(APIView):
    
    @extend_schema(responses={200: {"type": "array"}})
    def get(self, request: Request):
        query = request.query_params.get("q", "").strip()
        if not query:
            return Response([], status.HTTP_200_OK)

        artists = Artist.objects.filter(Q(name__icontains=query) | Q(persian_name__icontains=query))[:5]
        categories = Category.objects.filter(Q(name__icontains=query) | Q(persian_name__icontains=query))[:5]
        arts = Art.objects.filter(Q(name__icontains=query) | Q(persian_name__icontains=query))[:5]

        results = []

        for artist in artists:
            results.append({"type": "artist", 
                            "name": artist.name,
                            "persian_name": artist.persian_name, 
                            "slug": artist.slug})

        for category in categories:
            results.append({"type": "category", 
                            "name": category.name,
                            "persian_name": artist.persian_name, 
                            "slug": category.slug})

        for art in arts:
            results.append({"type": "art", 
                            "name": art.name,
                            "persian_name": artist.persian_name, 
                            "slug": art.slug, 
                            "image": art.image.url if art.image else None,})

        return Response(results, status.HTTP_200_OK)

class ArtFilterOptionsView(APIView):

    @extend_schema(responses={200: {"type": "object"}})
    def get(self, request: Request):
        tags_by_type = {}
        for tag_type, label in Tag.TagType.choices:
            tags_by_type[tag_type] = list(Tag.objects.filter(type=tag_type).values("id", "name"))

        years = list(
            Art.objects.exclude(released_year__isnull=True)
            .values_list("released_year", flat=True)
            .distinct()
            .order_by("-released_year")
        )

        artists = list(Artist.objects.values("id", "name", "slug"))

        shapes = [
            {"value": "square", "label": "مربع"},
            {"value": "horizontal", "label": "مستطیل افقی"},
            {"value": "vertical", "label": "مستطیل عمودی"},
        ]

        return Response({
            "tags": tags_by_type,
            "years": years,
            "artists": artists,
            "shapes": shapes,
        }, status.HTTP_200_OK)


from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *
from accounts.authentication import user_authenticate

class BackgroundImageListView(APIView):

    def get(self, request: Request):
        backgrounds = BackgroundImage.objects.all().order_by('-created_at')
        serializer = BackgroundImageSerializer(backgrounds, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request):
        user = user_authenticate(request)

        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)

        serializer = BackgroundImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "تصویر پس‌زمینه با موفقیت اضافه شد"}, status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request):
        user = user_authenticate(request)

        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)

        ids = request.data.get('ids')

        if not isinstance(ids, list) or not ids:
            return Response({"detail": "ids must be a non-empty list."}, status.HTTP_400_BAD_REQUEST)

        backgrounds = BackgroundImage.objects.filter(id__in=ids)
        
        deleted_count, _ = backgrounds.delete()

        return Response({"detail": "تصاویر با موفقیت حذف شدند", "deleted_count": deleted_count},status.HTTP_200_OK)


class BackgroundImageDetailView(APIView):

    def get_object(self, pk):
        try:
            return BackgroundImage.objects.get(pk=pk)
        except BackgroundImage.DoesNotExist:
            return None

    def get(self, request: Request, pk):
        background = self.get_object(pk)

        if background is None:
            return Response({"detail": "تصویر پس‌زمینه پیدا نشد"}, status.HTTP_404_NOT_FOUND)

        serializer = BackgroundImageSerializer(background)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, pk):
        user = user_authenticate(request)

        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)

        background = self.get_object(pk)

        if background is None:
            return Response({"detail": "تصویر پس‌زمینه پیدا نشد"}, status.HTTP_404_NOT_FOUND)

        background.delete()
        return Response({"detail": "تصویر پس‌زمینه با موفقیت حذف شد"}, status.HTTP_200_OK)
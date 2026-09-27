from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .serializers import *

from .authentication import user_authenticate

import secrets
from django.core.cache import cache

from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken

from art.models import Art


class ProfileView(APIView):
    
    def get(self, request: Request):
        user = user_authenticate(request)
        user = request.user
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request: Request):
        user= user_authenticate(request)
        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "اطلاعات با موفقیت بروز شد"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RequestOTPView(APIView):

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data["phone"]
            otp = str(secrets.randbelow(900000) + 100000)
            cache.set(f"otp:{phone}",otp,timeout=120)
            return Response({**serializer.data, "otp": otp}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

User = get_user_model()

class VerifyOTPView(APIView):

    def post(self, request: Request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data["phone"]
        otp = serializer.validated_data["otp"]

        saved_otp = cache.get(f"otp:{phone}")

        if saved_otp is None:
            return Response({"detail": "کد یکبار مصرف نادرست است یا منقضی شده است"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        if saved_otp != otp:
            return Response({"detail": "کد یکبار مصرف نادرست است یا منقضی شده است"},
                            status=status.HTTP_400_BAD_REQUEST)


        cache.delete(f"otp:{phone}")
        user, created = User.objects.get_or_create(phone=phone)

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })


class LogoutView(APIView):

    def post(self, request: Request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"detail": "رفرش توکن وده"},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"detail": "با موفقیت از خارج شدید"},
                status=status.HTTP_200_OK)

        except Exception:
            return Response(
                {"detail": "رفرش توکنت خرابه"},
                status=status.HTTP_400_BAD_REQUEST)


class FavoriteArtsView(APIView):

    def get(self, request):
        user = user_authenticate(request)

        arts = user.favorite_arts.all()
        serializer = FavoriteArtsSerializer(arts, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, slug):
        user = user_authenticate(request)

        try:
            art = Art.objects.get(slug=slug)
        except Art.DoesNotExist:
            return Response({"detail": "Art not found."}, status.HTTP_404_NOT_FOUND)

        user.favorite_arts.add(art)

        return Response({"detail": "Art added to favorites."}, status.HTTP_200_OK)

    def delete(self, request, slug):
        user = user_authenticate(request)

        try:
            art = Art.objects.get(slug=slug)
        except Art.DoesNotExist:
            return Response({"detail": "Art not found."}, status.HTTP_404_NOT_FOUND)

        user.favorite_arts.remove(art)

        return Response({"detail": "Art removed from favorites."}, status.HTTP_200_OK)
    


class AddressView(APIView):

    def get(self, request: Request):
        user = user_authenticate(request)
        addresses = Address.objects.filter(user=user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request):
        user = user_authenticate(request)
        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response({"detail":"آدرس شما اضافه شد"}, status.HTTP_201_CREATED)


class AddressDetailView(APIView):

    def patch(self, request: Request, pk):
        user = user_authenticate(request)

        try:
            address = Address.objects.get(pk=pk, user=user)
        except Address.DoesNotExist:
            return Response({"detail": "Address not found."}, status.HTTP_404_NOT_FOUND)

        serializer = AddressSerializer(address, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, pk):
        user = user_authenticate(request)

        try:
            address = Address.objects.get(pk=pk, user=user)
        except Address.DoesNotExist:
            return Response({"detail": "Address not found."}, status.HTTP_404_NOT_FOUND)

        address.delete()
        return Response({"detail":"آدرس با موفقیت حذف شد"}, status.HTTP_200_OK)
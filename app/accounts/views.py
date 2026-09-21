from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .serializers import ProfileSerializer, RequestOTPSerializer, VerifyOTPSerializer, ProfileUpdateSerializer

from .authentication import user_authenticate

import secrets
from django.core.cache import cache

from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken


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
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .serializers import PriceBaseSerializer, DiscountCodeSerializer
from .models import PriceBase, DiscountCode

from accounts.authentication import user_authenticate


class PriceBaseView(APIView):
    
    def get(self, request:Request):
        
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)
        
        price_bases  = PriceBase.objects.all()
        
        data = {price_base.type: price_base.price for price_base in price_bases}
        data = {
            price_base.type: {
                "price": price_base.price,
                "updated_at": price_base.updated_at}
            for price_base in price_bases}
        
        return Response(data, status=status.HTTP_200_OK)
    
    def patch(self, request:Request):
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)
        
        serializer = PriceBaseSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        for price_type, price in serializer.validated_data.items():
            price_base = PriceBase.objects.get(type=price_type)
            price_base.price = price
            price_base.save()

        return Response({"detail": "Price bases updated successfully."}, status.HTTP_200_OK)
    


class DiscountCodeListView(APIView):
    
    def get(self, request:Request):
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)
        
        discount_codes  = DiscountCode.objects.all()
        serializer = DiscountCodeSerializer(discount_codes, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
            
    def post(self, request:Request):
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)
        
        serializer = DiscountCodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail":"کد تخفیف جدید ساخته شد"}, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        
class DiscountCodeDetailView(APIView):
    
    def get_object(self, pk):
        try:
            return DiscountCode.objects.get(pk=pk)
        except DiscountCode.DoesNotExist:
            return None

        
    def get(self, request:Request, pk):
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)
        
        discount_code = self.get_object(pk)
        if discount_code is None:
            return Response({"detail": "تخفیف پیدا نشد"}, status.HTTP_404_NOT_FOUND)
        
        serializer = DiscountCodeSerializer(discount_code)
        return Response(serializer.data, status.HTTP_200_OK)
        
    def put(self, request:Request, pk):
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)
        
        discount_code = self.get_object(pk)
        if discount_code is None:
            return Response({"detail": "تخفیف پیدا نشد"}, status.HTTP_404_NOT_FOUND)

        serializer = DiscountCodeSerializer(discount_code, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail":"کد تخفیف با موفقیت ویرایش شد"}, status.HTTP_200_OK)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            
    def delete(self, request:Request, pk):
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)
        
        discount_code = self.get_object(pk)
        if discount_code is None:
            return Response({"detail": "تخفیف پیدا نشد"}, status.HTTP_404_NOT_FOUND)

        discount_code.delete()
        return Response({"detail":"کد تخفیف با موفقیت حذف شد"}, status.HTTP_200_OK)
    

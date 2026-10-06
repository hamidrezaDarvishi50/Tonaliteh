from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

from accounts.authentication import user_authenticate
from .services import calculate_art_price, refresh_cart, get_price_bases
from drf_spectacular.utils import extend_schema

class CartView(APIView):

    @extend_schema(
        responses={200: CartSerializer,})
    def get(self, request:Request):
        user = user_authenticate(request)
        cart, _ = Cart.objects.get_or_create(user=user)
        refresh_cart(cart)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status.HTTP_200_OK)

class CartItemView(APIView):
    
    @extend_schema(
        request=CartItemSerializer,
        responses={
            201: CartItemSerializer,
            200: CartItemSerializer,
            401: {"type": "object"},
            400: {"type": "object"},})
    def post(self, request):
        user = user_authenticate(request)

        cart, _ = Cart.objects.get_or_create(user=user)

        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        art = serializer.validated_data["art"]
        frame = serializer.validated_data["frame"]
        passepartout = serializer.validated_data["passepartout"]
        quantity = serializer.validated_data["quantity"]

        price_bases = get_price_bases()

        unit_price = calculate_art_price(art, frame, passepartout, price_bases)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            art=art,
            frame=frame,
            passepartout=passepartout,
            defaults={"quantity": quantity, "unit_price": unit_price,}
        )

        if not created:
            item.quantity += quantity
            item.save(update_fields=["quantity", "updated_at"])

        refresh_cart(cart)

        return Response(
            CartItemSerializer(item).data, status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class CartItemDetailView(APIView):

    @extend_schema(
        responses={
            200: CartItemSerializer,
            401: {"type": "object"},
            404: {"type": "object"},})
    def get(self, request:Request, pk):
        user = user_authenticate(request)

        try:
            item = CartItem.objects.select_related("art", "frame", "passepartout"
                ).get(pk=pk, cart__user=user)
            
        except CartItem.DoesNotExist:
            return Response({"detail": "Cart item not found."}, status.HTTP_404_NOT_FOUND)

        serializer = CartItemSerializer(item)
        return Response(serializer.data, status.HTTP_200_OK)
    
    @extend_schema(
        responses={
            200: {"type": "object"},
            401: {"type": "object"},
            404: {"type": "object"},})
    def delete(self, request:Request, pk):
        user = user_authenticate(request)

        try:
            item = CartItem.objects.get(pk=pk, cart__user=user)
        except CartItem.DoesNotExist:
            return Response({"detail": "Cart item not found."}, status.HTTP_404_NOT_FOUND)

        cart = item.cart
        item.delete()

        refresh_cart(cart)

        return Response({"detail": "موفقیت آمیز بود"}, status.HTTP_200_OK)
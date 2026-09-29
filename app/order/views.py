from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from Cart.models import Cart
from Cart.services import refresh_cart

from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer, DiscountCodeCheckSerializer
from .services import create_order_from_cart, get_valid_discount_code, calculate_discount_amount

from accounts.authentication import user_authenticate


class OrderListCreateView(APIView):

    def get(self, request: Request):
        user = user_authenticate(request)
        orders = Order.objects.filter(user=user).prefetch_related("items").order_by("-created_at")

        status_param = request.query_params.get("status")
        if status_param:
            orders = orders.filter(status=status_param)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request):
        user = user_authenticate(request)

        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            order = create_order_from_cart(
                user=user,
                address_id=data["address"],
                destination=data["destination"],
                discount_code_str=data.get("discount_code"),
            )
        except ValueError as e:
            return Response({"detail": str(e)}, status.HTTP_400_BAD_REQUEST)

        return Response({"detail":"سبد سفارشات جدید با موفقیت ایجاد شد"}, status.HTTP_201_CREATED)


class OrderDetailView(APIView):

    def get(self, request: Request, pk):
        user = user_authenticate(request)
        try:
            order = Order.objects.prefetch_related("items").get(pk=pk, user=user)
        except Order.DoesNotExist:
            return Response({"detail": "سفارش پیدا نشد"}, status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status.HTTP_200_OK)


class OrderCancelView(APIView):

    def post(self, request: Request, pk):
        user = user_authenticate(request)
        try:
            order = Order.objects.get(pk=pk, user=user)
        except Order.DoesNotExist:
            return Response({"detail": "سفارش پیدا نشد"}, status.HTTP_404_NOT_FOUND)

        try:
            order.cancel()
        except ValueError as e:
            return Response({"detail": str(e)}, status.HTTP_400_BAD_REQUEST)

        return Response({"detail":"سفارش لغو شد"}, status.HTTP_200_OK)


class DiscountCodeCheckView(APIView):

    def post(self, request: Request):
        user = user_authenticate(request)
        serializer = DiscountCodeCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = Cart.objects.filter(user=user).first()
        if cart is None or not cart.items.exists():
            return Response({"detail": "سبد خرید شما خالی است"}, status.HTTP_400_BAD_REQUEST)

        refresh_cart(cart)
        items_price = sum(item.unit_price * item.quantity for item in cart.items.all())

        try:
            discount = get_valid_discount_code(serializer.validated_data["code"])
        except ValueError as e:
            return Response({"detail": str(e)}, status.HTTP_400_BAD_REQUEST)

        discount_amount = calculate_discount_amount(discount, items_price)

        return Response({
            "code": discount.code,
            "type": discount.type,
            "discount_amount": discount_amount,
        }, status.HTTP_200_OK)


class AdminOrderStatusView(APIView):

    ACTIONS = {
        "ship": "mark_as_shipped",
        "complete": "mark_as_completed",
        "cancel": "cancel",
    }

    def post(self, request: Request, pk):
        user = user_authenticate(request)
        if not user.is_staff:
            return Response({"detail": "Admin access required."}, status.HTTP_403_FORBIDDEN)

        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"detail": "سفارش پیدا نشد"}, status.HTTP_404_NOT_FOUND)

        method_name = self.ACTIONS.get(request.data.get("action"))
        if method_name is None:
            return Response({"detail": "عملیات نامعتبر است"}, status.HTTP_400_BAD_REQUEST)

        try:
            getattr(order, method_name)()
        except ValueError as e:
            return Response({"detail": str(e)}, status.HTTP_400_BAD_REQUEST)

        return Response(OrderSerializer(order).data)
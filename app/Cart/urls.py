from django.urls import path

from .views import *

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("items/", CartItemView.as_view(), name="cart-item-create"),
    path("items/<int:pk>/", CartItemDetailView.as_view(), name="cart-item-detail"),
]
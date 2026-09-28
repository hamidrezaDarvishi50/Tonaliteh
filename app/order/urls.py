from django.urls import path
from .views import *

urlpatterns = [
    path("orders/", OrderListCreateView.as_view()),
    path("orders/<int:pk>/", OrderDetailView.as_view()),
    path("orders/<int:pk>/cancel/", OrderCancelView.as_view()),
    path("orders/<int:pk>/admin-status/", AdminOrderStatusView.as_view()),
    path("orders/check-discount/", DiscountCodeCheckView.as_view()),
]
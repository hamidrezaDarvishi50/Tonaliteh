from django.urls import path
from .views import *

urlpatterns = [
    path("", OrderListCreateView.as_view()),
    path("<int:pk>/", OrderDetailView.as_view()),
    path("<int:pk>/cancel/", OrderCancelView.as_view()),
    path("<int:pk>/admin-status/", AdminOrderStatusView.as_view()),
    path("check-discount/", DiscountCodeCheckView.as_view()),
]
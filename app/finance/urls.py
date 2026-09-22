from django.urls import path
from .views import PriceBaseView, DiscountCodeListView, DiscountCodeDetailView

urlpatterns = [
    path("price-bases/", PriceBaseView.as_view(), name="price-bases"),
    
    path("discount-code/", DiscountCodeListView.as_view(), name="discount-codes"),
    path("discount-code/<int:pk>/", DiscountCodeDetailView.as_view())
]

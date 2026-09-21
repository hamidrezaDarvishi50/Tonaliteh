from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RequestOTPView, VerifyOTPView, ProfileView, LogoutView, FavoriteArtsView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='Profile'),
    path('refresh/', TokenRefreshView.as_view(), name='Refresh'),
    path("request-otp/", RequestOTPView.as_view(), name="request-otp"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("logout/", LogoutView.as_view(), name="logout"),
    
    path("favorites/", FavoriteArtsView.as_view(), name="favorites"),
    path("favorites/<slug:slug>/", FavoriteArtsView.as_view(), name="favorite-art")
]
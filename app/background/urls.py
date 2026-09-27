from django.urls import path
from .views import *

urlpatterns = [
    path("",BackgroundImageListView.as_view(), name="background-list"),
    path("<int:pk>/", BackgroundImageDetailView.as_view(), name="background-detail"),
]
from django.urls import path
from .views import ArtistListView, ArtistDetailView, ArtListView, ArtDetailView, CategoryListView, CategoryDetailView

urlpatterns = [
    path("artists/", ArtistListView.as_view(), name="artists"),
    path("artists/<slug:slug>/", ArtistDetailView.as_view()),

    path("categories/", CategoryListView.as_view(), name="categories"),
    path("categories/<slug:slug>/", CategoryDetailView.as_view()),
    
    path("arts/", ArtListView.as_view(), name="arts"),
    path("arts/<slug:slug>/", ArtDetailView.as_view()),
]
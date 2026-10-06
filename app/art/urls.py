from django.urls import path
from .views import *

urlpatterns = [
    path("artists/", ArtistListView.as_view(), name="artists"),
    path("artists/<slug:slug>/", ArtistDetailView.as_view()),

    path("categories/", CategoryListView.as_view(), name="categories"),
    path("categories/<slug:slug>/", CategoryDetailView.as_view()),
    
    path("arts/", ArtListView.as_view(), name="arts"),
    path("arts/<slug:slug>/", ArtDetailView.as_view()),
    
    path("frame/", FrameListView.as_view(), name="frames"),
    path("frame/<int:pk>/", FrameDetailView.as_view()),
    
    path("passepartout/", PassepartoutListView.as_view(), name="passepartouts"),
    path("passepartout/<int:pk>/", PassepartoutDetailView.as_view()),
    
    path("tags/", TagListView.as_view()),
    path("tags/<int:pk>/", TagDetailView.as_view()),
    
    path("search/", SearchView.as_view()),
    path("arts-filter-options/", ArtFilterOptionsView.as_view()),
    
    path("arts-backup/", ArtBackupView.as_view()),
    path("artists-backup/", ArtistBackupView.as_view()),
]
from django.urls import path
from .views import *

urlpatterns = [
    path("<slug:slug>/", BlogDetailView.as_view()),
    path("", BlogView.as_view(), name='blogs')
]

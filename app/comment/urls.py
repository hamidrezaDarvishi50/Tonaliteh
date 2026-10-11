from django.urls import path
from .views import *

urlpatterns = [
    path("" ,CommentListView.as_view(), name="comments")
]

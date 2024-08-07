from django.urls import path
from .views import HomePage, PostDetailPage, CreateNewPostPage

app_name = "feed"

urlpatterns = [
    path("", HomePage.as_view(), name="index"),
    path("<int:pk>/", PostDetailPage.as_view(), name="detail"),
    path("new/", CreateNewPostPage.as_view(), name="new_post")
]
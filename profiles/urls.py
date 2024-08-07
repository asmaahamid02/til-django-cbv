from django.urls import path
from .views import ProfileDetailPage, FollowPage, ProfileUpdatePage

app_name = 'profiles'

urlpatterns = [
    path('<str:username>/', ProfileDetailPage.as_view(), name='detail'),
    path('<str:username>/edit', ProfileUpdatePage.as_view(), name='edit'),
    path('<str:username>/follow/', FollowPage.as_view(), name='follow'),
]
from django.urls import path

from .views import UserCommunityView, PublicProfileView

app_name = 'community'

urlpatterns = [
    path('search/', UserCommunityView.as_view(), name='search'),
    path('@<str:username>/', PublicProfileView.as_view(), name='public-user-profile'),
    path('', UserCommunityView.as_view(), name='community-list')
]

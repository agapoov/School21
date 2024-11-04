from django.urls import path
from .views import UserCommunityView

app_name = 'community'

urlpatterns = [
    path('search/', UserCommunityView.as_view(), name='search'),
    path('', UserCommunityView.as_view(), name='community-list')
]

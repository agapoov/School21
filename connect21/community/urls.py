from django.urls import path

from .views import PublicProfileView, UserCommunityView, invite_user

app_name = 'community'

urlpatterns = [
    path('search/', UserCommunityView.as_view(), name='search'),
    path('@<str:username>/', PublicProfileView.as_view(), name='public-user-profile'),
    path('', UserCommunityView.as_view(), name='community-list'),
    path('invite/<int:user_id>/<int:group_id>/', invite_user, name='invite_user')

]

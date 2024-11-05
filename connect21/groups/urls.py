from django.urls import path
from .views import chat_view

app_name = 'groups'

urlpatterns = [
    path('chat/<str:group_name>/', chat_view, name='group_chat'),

]
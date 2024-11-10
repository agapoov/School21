from django.urls import path

from .views import chat_view

app_name = 'groups'

urlpatterns = [
    path('chat/<uuid:group_uuid>/', chat_view, name='group_chat'),

]
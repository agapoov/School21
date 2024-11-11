from django.urls import path

from .views import CreateGroupView, DeleteChatView, chat_view

app_name = 'groups'

urlpatterns = [
    path('chat/<uuid:group_uuid>/', chat_view, name='group_chat'),
    path('create/', CreateGroupView.as_view(), name='create_chat'),
    path('delete/<uuid:uuid>/', DeleteChatView.as_view(), name='delete_chat'),

]

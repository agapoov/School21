from django.contrib import admin
from .models import ChatGroup, GroupMembership, GroupInvitation, ChatMessage

admin.site.register(ChatGroup)
admin.site.register(GroupMembership)
admin.site.register(GroupInvitation)
admin.site.register(ChatMessage)

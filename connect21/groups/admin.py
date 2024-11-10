from django.contrib import admin

from .models import ChatGroup, ChatMessage, GroupInvitation, GroupMembership


@admin.register(ChatGroup)
class ChatGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'uuid')
    search_fields = ('name', 'uuid')
    readonly_fields = ('uuid',)


admin.site.register(GroupMembership)
admin.site.register(GroupInvitation)
admin.site.register(ChatMessage)

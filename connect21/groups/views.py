from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View

from .models import ChatGroup, GroupMembership, GroupInvitation, ChatMessage


# @login_required
# def create_group(request):
#     if request.method == 'POST':
#         group_name = request.POST.get('group_name')
#         if group_name:
#             group = ChatGroup.objects.create(name=group_name, created_by=request.user)
#             GroupMembership.objects.create(user=request.user, group=group)
#             messages.success(request, 'Группа успешно создана!')
#             return redirect('group_detail', group_id=group.id)
#         else:
#             messages.error(request, 'Введите имя группы.')
#     return render(request, 'create_group.html')


def chat_view(request, group_name):
    group = get_object_or_404(ChatGroup, name=group_name)
    messages = ChatMessage.objects.filter(group=group).order_by('timestamp')
    return render(request, 'groups/chat.html', {
        'group_name': group_name,
        'messages': messages
    })

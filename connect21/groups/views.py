from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .models import ChatGroup, ChatMessage, GroupMembership

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

    if not GroupMembership.objects.filter(group=group, user=request.user).exists():
        return HttpResponseForbidden("Access Denied. You are not a member of this group.")

    messages = ChatMessage.objects.filter(group=group).order_by('timestamp')
    request.session['user_id'] = request.user.id
    return render(request, 'groups/chat.html', {
        'group_name': group_name,
        'messages': messages,
        'title': f'Connect21 - Чат {group_name}'
    })

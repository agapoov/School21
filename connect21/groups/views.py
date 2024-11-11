from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from main.mixins import TitleMixin

from .forms import CreateGroupForm
from .models import ChatGroup, ChatMessage, GroupMembership


class CreateGroupView(TitleMixin, FormView):
    template_name = 'groups/create_group.html'
    form_class = CreateGroupForm
    title = 'Connect21 - Создание группы'
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        group = form.save(commit=False)
        group.created_by = self.request.user
        group.save()

        GroupMembership.objects.create(group=group, user=self.request.user)
        messages.success(self.request, f'Вы успешно создали группу {group.name}')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Заполните все поля правильно')
        return super().form_invalid(form)


class DeleteChatView(LoginRequiredMixin, UserPassesTestMixin, View):
    model = ChatGroup

    def test_func(self):
        chat = self.get_object()
        return chat.created_by == self.request.user

    def get_object(self):
        uuid = self.kwargs.get('uuid')
        return get_object_or_404(ChatGroup, uuid=uuid)

    def post(self, request, *args, **kwargs):
        group = self.get_object()
        group.delete()
        messages.success(self.request, f'Вы успешно удалили группу {group.name}')
        return redirect(reverse_lazy('main:index'))


def chat_view(request, group_uuid):
    group = get_object_or_404(ChatGroup, uuid=group_uuid)

    if not GroupMembership.objects.filter(group=group, user=request.user).exists():
        return HttpResponseForbidden("Access Denied. You are not a member of this group.")

    messages = ChatMessage.objects.filter(group=group).order_by('timestamp')
    request.session['user_id'] = request.user.id
    return render(request, 'groups/chat.html', {
        'group': group,
        'messages': messages,
        'title': f'Connect21 - Чат {group.name}'
    })

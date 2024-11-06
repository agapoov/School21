from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
from django.db.models import Q
from groups.models import ChatGroup, GroupInvitation, GroupMembership
from users.models import User

from .utils import q_search


class UserCommunityView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'community/community_list.html'
    context_object_name = 'users'
    paginate_by = 2
    allow_empty = False

    def get_queryset(self):
        queryset = User.objects.all().order_by('-username')
        query = self.request.GET.get('q')
        if query:
            return q_search(query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список пользователей'
        return context


class PublicProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'community/public_profile.html'
    context_object_name = 'user_public_profile'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_groups = GroupMembership.objects.filter(user=self.request.user).select_related('group')
        context['user_groups'] = [membership.group for membership in user_groups]
        return context


@login_required
def invite_user(request, user_id, group_id):
    invited_user = get_object_or_404(User, id=user_id)
    group = get_object_or_404(ChatGroup, id=group_id)

    if request.method == 'POST':
        if GroupMembership.objects.filter(group=group, user=invited_user).exists() or \
                GroupInvitation.objects.filter(
                    Q(group=group) & Q(receiver=invited_user) & Q(status="pending")
                ).exists():
            messages.warning(request, 'Пользователь является членом группы или уже был в нее приглашен.')
            return HttpResponseRedirect(request.META['HTTP_REFERER'])

        GroupInvitation.objects.create(
            group=group,
            sender=request.user,  # TODO сделать отправку писем о состоянии приглашения
            receiver=invited_user,
            status="pending"
        )
        # TODO отправка письма о приглашении получателю
        messages.success(request, f'Вы пригласили пользователя {invited_user.username} в чат')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    return HttpResponse(status=405)

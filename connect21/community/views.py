from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView

from groups.models import ChatGroup, GroupMembership
from main.mixins import TitleMixin
from users.models import User

from .utils import check_and_invite_user, q_search


class UserCommunityView(TitleMixin, LoginRequiredMixin, ListView):
    title = 'Connect21 - Список пользователей'
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


class PublicProfileView(TitleMixin, LoginRequiredMixin, DetailView):
    model = User
    title = 'Connect21 - Профиль пользователя'
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
@require_POST
def invite_user(request, user_id, group_id):
    try:
        invited_user = get_object_or_404(User, id=user_id)
        group = get_object_or_404(ChatGroup, id=group_id)

        if check_and_invite_user(request, invited_user, group):
            messages.success(request, f'Вы пригласили пользователя {invited_user.username} в чат')
        else:
            messages.warning(request, 'Пользователь является членом группы или уже был в нее приглашен.')

    except ObjectDoesNotExist:
        messages.warning(request, 'Пользователя или группы не существует.')
    except Exception as e:
        messages.warning(request, f'Непредвиденная ошибка: {str(e)}')

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

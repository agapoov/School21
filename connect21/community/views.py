from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

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

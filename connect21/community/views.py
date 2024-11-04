from .utils import q_search
from django.views.generic import ListView
from users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


class UserCommunityView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'community/community_list.html'
    context_object_name = 'users'
    paginate_by = 2
    allow_empty = False

    def get_queryset(self):
        queryset = User.objects.all()

        query = self.request.GET.get('q')
        if query:
            return q_search(query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список пользователей'
        return context

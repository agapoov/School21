from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .forms import CustomUserLoginForm


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = CustomUserLoginForm
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        user = form.get_user()
        messages.success(self.request, f'С возвращением {user.username}.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Неверный Юзернейм или пароль.')
        return super().form_invalid(form)

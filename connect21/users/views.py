from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from .forms import CustomUserLoginForm, CustomUserCreationForm


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


class CustomRegisterView(CreateView):
    template_name = 'users/registration.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Вы успешно зарегистрированы. Теперь войдите.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Неправильно заполнены поля')
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    def get_success_url(self):
        messages.success(self.request, 'Вы вышли из аккаунта')
        return reverse_lazy('main:index')

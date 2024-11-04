from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, UpdateView

from .forms import (CustomUserCreationForm, CustomUserLoginForm,
                    TwoFactorLoginForm, CustomUserProfileForm)
from .mixins import UserVerificationMixin
from .models import User


class CustomLoginView(UserVerificationMixin, LoginView):
    template_name = 'users/login.html'
    authentication_form = CustomUserLoginForm
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        user = form.get_user()
        verification_uuid = self.handle_verification(user)
        return redirect('users:two-factor-auth', uuid=verification_uuid)

    def form_invalid(self, form):
        messages.warning(self.request, 'Неверный Юзернейм или пароль.')
        return super().form_invalid(form)


class CustomRegisterView(UserVerificationMixin, CreateView):
    template_name = 'users/registration.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        verification_uuid = self.handle_verification(user)
        return redirect('users:two-factor-auth', uuid=verification_uuid)

    def form_invalid(self, form):
        messages.warning(self.request, 'Неправильно заполнены поля')
        return super().form_invalid(form)


class TwoFactorAuthView(View):
    def get(self, request, uuid):
        form = TwoFactorLoginForm()
        return render(request, 'users/two_factor_auth.html', {'form': form, 'uuid': uuid})

    def post(self, request, uuid):
        form = TwoFactorLoginForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            timestamp = request.session.get('timestamp')
            if timestamp and (timezone.now() - timestamp) > timedelta(minutes=5):
                return render(request, 'users/two_factor_auth.html', {'form': form, 'error': 'Код истек', 'uuid': uuid})

            if str(code) == str(request.session.get('two_factor_code')):
                user_id = request.session.get('user_id')
                user = User.objects.get(id=user_id)
                login(request, user)
                messages.success(request, 'Добро пожаловать')
                del request.session['two_factor_code']
                del request.session['user_id']
                del request.session['verification_uuid']
                return redirect('main:index')
            else:
                return render(request, 'users/two_factor_auth.html', {'form': form, 'error': 'Неверный код', 'uuid': uuid})
        return render(request, 'users/two_factor_auth.html', {'form': form, 'uuid': uuid})


class CustomProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = CustomUserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_free = form.cleaned_data.get('available')
        user.save()
        messages.success(self.request, 'Профиль успешно обновлен')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Произошла ошибка')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование профиля'
        return context


class CustomLogoutView(LogoutView):
    def get_success_url(self):
        messages.success(self.request, 'Вы вышли из аккаунта')
        return reverse_lazy('main:index')

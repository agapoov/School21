from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.views.generic.edit import FormView
from .forms import (CustomUserCreationForm, CustomUserLoginForm,
                    CustomUserProfileForm, TwoFactorLoginForm)
from .mixins import UserVerificationMixin
from .models import User
from main.mixins import TitleMixin


class CustomLoginView(TitleMixin, UserVerificationMixin, LoginView):
    template_name = 'users/login.html'
    authentication_form = CustomUserLoginForm
    title = 'Connect21 - Вход'
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        user = form.get_user()
        verification_uuid = self.handle_verification(user)
        return redirect('users:two-factor-auth', uuid=verification_uuid)

    def form_invalid(self, form):
        messages.warning(self.request, 'Неверный Юзернейм или пароль.')
        return super().form_invalid(form)


class CustomRegisterView(TitleMixin, UserVerificationMixin, CreateView):
    template_name = 'users/registration.html'
    form_class = CustomUserCreationForm
    title = 'Connect21 - Регистрация '
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        verification_uuid = self.handle_verification(user)
        return redirect('users:two-factor-auth', uuid=verification_uuid)


class TwoFactorAuthView(TitleMixin, FormView):
    title = 'Connect - 2FA Auth'
    form_class = TwoFactorLoginForm
    template_name = 'users/two_factor_auth.html'

    def get_initial(self):
        return {'uuid': self.kwargs['uuid']}

    def form_valid(self, form):
        code = form.cleaned_data['code']
        timestamp = self.request.session.get('timestamp')

        if timestamp and (timezone.now() - timestamp) > timedelta(minutes=5):
            form.add_error(None, 'Код истек. Войдите заново.')
            return self.form_invalid(form)

        if str(code) == str(self.request.session.get('two_factor_code')):
            user_id = self.request.session.get('user_id')
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                form.add_error(None, 'Пользователь не найден.')
                return self.form_invalid(form)

            login(self.request, user)
            messages.success(self.request, 'Добро пожаловать')

            self._clear_session()
            return super().form_valid(form)

        form.add_error(None, 'Неверный код')
        return self.form_invalid(form)

    def _clear_session(self):
        keys_to_clear = ['two_factor_code', 'user_id', 'verification_uuid']
        for key in keys_to_clear:
            self.request.session.pop(key, None)

    def get_success_url(self):
        return reverse('main:index')

# class TwoFactorAuthView(TitleMixin, View):
#     title = 'Connect21 - 2FA Auth'
#
#     def get(self, request, uuid):
#         form = TwoFactorLoginForm()
#         return render(request, 'users/two_factor_auth.html', {'form': form, 'uuid': uuid})
#
#     def post(self, request, uuid):
#         form = TwoFactorLoginForm(request.POST)
#         if form.is_valid():
#             code = form.cleaned_data['code']
#             timestamp = request.session.get('timestamp')
#             if timestamp and (timezone.now() - timestamp) > timedelta(minutes=5):
#                 return render(request, 'users/two_factor_auth.html', {'form': form, 'error': 'Код истек. Войдите '
#                                                                                              'заново.', 'uuid': uuid})
#
#             if str(code) == str(request.session.get('two_factor_code')):
#                 user_id = request.session.get('user_id')
#                 user = User.objects.get(id=user_id)
#                 login(request, user)
#                 messages.success(request, 'Добро пожаловать')
#                 del request.session['two_factor_code']
#                 del request.session['user_id']
#                 del request.session['verification_uuid']
#                 return redirect('main:index')
#             else:
#                 return render(request, 'users/two_factor_auth.html', {'form': form, 'error': 'Неверный код', 'uuid': uuid})
#         return render(request, 'users/two_factor_auth.html', {'form': form, 'uuid': uuid})


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


def forgot_password(request):
    return render(request, 'users/forgot_password.html')


class CustomLogoutView(LogoutView):
    def get_success_url(self):
        messages.success(self.request, 'Вы вышли из аккаунта')
        return reverse_lazy('main:index')

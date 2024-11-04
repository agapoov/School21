from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from .forms import CustomUserLoginForm, CustomUserCreationForm, TwoFactorLoginForm
from django.views import View
from .models import User
import uuid
from django.utils import timezone
from datetime import timedelta

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = CustomUserLoginForm
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        user = form.get_user()
        verification_code = user.generate_code()
        user.send_verification_email(verification_code)

        self.request.session['two_factor_code'] = verification_code
        self.request.session['user_id'] = user.id

        verification_uuid = uuid.uuid4()
        self.request.session['verification_uuid'] = str(verification_uuid)

        return redirect('users:two-factor-auth', uuid=verification_uuid)

    def form_invalid(self, form):
        messages.warning(self.request, 'Неверный Юзернейм или пароль.')
        return super().form_invalid(form)


class CustomRegisterView(CreateView):
    template_name = 'users/registration.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        verification_code = user.generate_code()
        user.send_verification_email(verification_code)
        self.request.session['two_factor_code'] = verification_code
        self.request.session['user_id'] = user.id
        verification_uuid = uuid.uuid4()
        self.request.session['verification_uuid'] = str(verification_uuid)
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


class CustomLogoutView(LogoutView):
    def get_success_url(self):
        messages.success(self.request, 'Вы вышли из аккаунта')
        return reverse_lazy('main:index')

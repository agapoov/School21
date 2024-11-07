from datetime import datetime, timedelta

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils import timezone

from connect21.settings import CODE_LIFETIME_MINUTES

from .models import User


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Имя пользователя'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Пароль'
    )


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Имя'
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Фамилия'
    )
    surname = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Отчество',
    )
    gender = forms.ChoiceField(
        choices=[('M', 'Мужской'), ('F', 'Женский')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Пол'
    )
    age = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Возраст'
    )
    tg_username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Ник в @Telegram'
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Имя пользователя'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Электронная почта'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Пароль',
        required=True
    )
    password2= forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Подтверждение пароля',
        required=True
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'surname', 'gender', 'age', 'tg_username', 'username',
                  'email', 'password1', 'password2']


class TwoFactorLoginForm(forms.Form):
    code = forms.IntegerField(label='Код подтверждения')

    class TwoFactorLoginForm(forms.Form):
        code = forms.IntegerField(label='Код подтверждения')

        def clean_code(self):
            code = self.cleaned_data.get('code')
            timestamp_str = self.initial.get('timestamp')

            if not timestamp_str:
                raise forms.ValidationError('Время начала сессии не найдено. Попробуйте войти снова.')

            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
            timestamp = timezone.make_aware(timestamp, timezone.get_current_timezone())

            if (timezone.now() - timestamp) > timedelta(minutes=CODE_LIFETIME_MINUTES):
                raise forms.ValidationError('Код истек. Войдите заново.')

            if not code or len(str(code)) != 6:
                raise forms.ValidationError('Код должен состоять из 6 цифр.')

            return code


class CustomUserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'surname', 'gender', 'age', 'tg_username', 'username', 'email', 'interests', 'additional_info']
        widgets = {
            'interests': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'oninput': 'autoResize(this)', 'maxlength': '128'}),
            'additional_info': forms.Textarea(attrs={'rows': 6, 'cols': 40, 'oninput': 'autoResize(this)', 'maxlength': '512'}),
            'email': forms.EmailInput(attrs={'readonly': 'readonly'})
        }

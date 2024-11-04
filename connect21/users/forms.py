from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

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


class CustomUserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'surname', 'gender', 'age', 'tg_username', 'username', 'email', 'interests', 'additional_info']
        widgets = {
            'interests': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'oninput': 'autoResize(this)', 'maxlength': '128'}),
            'additional_info': forms.Textarea(attrs={'rows': 6, 'cols': 40, 'oninput': 'autoResize(this)', 'maxlength': '512'}),
            'email': forms.EmailInput(attrs={'readonly': 'readonly'})
        }
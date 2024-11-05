from django.urls import path

from .views import (CustomLoginView, CustomLogoutView, CustomProfileView,
                    CustomRegisterView, TwoFactorAuthView, forgot_password)

app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('profile/', CustomProfileView.as_view(), name='profile'),
    path('two-factor-auth/<uuid:uuid>', TwoFactorAuthView.as_view(), name='two-factor-auth'),
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('logout/', CustomLogoutView.as_view(), name='logout')
]
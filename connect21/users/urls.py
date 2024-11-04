from django.urls import path
from .views import CustomLoginView, CustomLogoutView, CustomRegisterView, TwoFactorAuthView

app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('two-factor-auth/<uuid:uuid>', TwoFactorAuthView.as_view(), name='two-factor-auth'),
    path('logout/', CustomLogoutView.as_view(), name='logout')
]
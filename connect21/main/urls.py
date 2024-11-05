from django.urls import path

from .views import about, home_page, respond_invitation

app_name = 'main'

urlpatterns = [
    path('', home_page, name='index'),
    path('about/', about, name='about'),
    path('invite/respond/<int:invitation_id>/', respond_invitation, name='respond_invitation'),
]

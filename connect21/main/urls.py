from django.urls import path

from .views import AboutView, HomeView, RespondInvitationView

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('invite/respond/<int:invitation_id>/', RespondInvitationView.as_view(), name='respond_invitation'),
]

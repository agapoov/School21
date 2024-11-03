from django.urls import path

from .views import about, home_page

app_name = 'main'

urlpatterns = [
    path('', home_page, name='index'),
    path('about/', about, name='about')
]

from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('usuarios/reservas', views.reservas_lista_api, name='reservas_lista_api'),
]


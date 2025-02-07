from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('reservas', views.reservas_lista_api, name='reservas_lista_api'),
    path('usuarios', views.usuarios_lista_api, name='usuarios_lista_api'),
    path('reservasMejoradas', views.reservasMejoradas_lista_api, name='reservasMejoradas_lista_api'),
    path('alojamientosMejorados', views.alojamientosMejorados_lista_api, name='alojamientosMejorados_lista_api'),
    path('transportesMejorados', views.transportesMejorados_lista_api, name='transportesMejorados_lista_api'),
    
    path('buscar-reservas/', views.reserva_busqueda_simple, name='reserva_busqueda_simple'),
    path('buscar-reservas-avanzada/', views.reserva_busqueda_avanzada, name='reserva_busqueda_avanzada'),
    path('buscar-usuario-avanzada/', views.usuario_busqueda_avanzada, name='usuario_busqueda_avanzada'),
    path('buscar-destino-avanzada/', views.destino_busqueda_avanzada, name='destino_busqueda_avanzada'),
    path('buscar-comentario-avanzada/', views.comentario_busqueda_avanzada, name='comentario_busqueda_avanzada'),
]


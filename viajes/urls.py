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
    path('buscar-alojamiento-avanzada/', views.alojamiento_busqueda_avanzada, name='alojamiento_busqueda_avanzada'),
    
    path('reservas/crear', views.reserva_crear, name='reserva_crear'),
    path('usuarios/crear', views.usuario_crear, name='usuario_crear'),
    path('transportes/crear', views.transporte_crear, name='transporte_crear'),
    
    path('reservas/editar/<int:reserva_id>/', views.reserva_editar, name='reserva_editar'),
    path('usuarios/editar/<int:usuario_id>/', views.usuario_editar, name='usuario_editar'),

    path('reserva/editar/codigo/<int:reserva_id>/', views.reserva_actualizar_codigo, name='reserva_actualizar_codigo'),
    path('usuario/editar/nombre/<int:usuario_id>/', views.usuario_actualizar_nombre, name='usuario_actualizar_nombre'),

    path('reserva/eliminar/<int:reserva_id>/', views.reserva_eliminar, name='reserva_eliminar'),
    path('usuario/eliminar/<int:usuario_id>/', views.usuario_eliminar, name='usuario_eliminar'),
]


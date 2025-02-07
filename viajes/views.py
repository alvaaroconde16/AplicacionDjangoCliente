from requests.exceptions import HTTPError
from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Q, Sum
from django.contrib import messages
from django.contrib.auth.models import Group
import requests

import requests
import environ
import os
from pathlib import Path
from .forms import *


BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()


# Create your views here.
def index(request):
    
    return render(request, 'principal.html')


def crear_cabecera():
    return {
        'Authorization': 'Bearer ' + env("OAUTH2_ACCESS_TOKEN"),
        "Content-Type": "application/json"
    }


def reservas_lista_api(request):
    headers = {'Authorization' : 'Bearer '+env('OAUTH2_ACCESS_TOKEN_ADMIN')}    
    response = requests.get('https://alvaroconde.pythonanywhere.com/api/v1/reservas', headers=headers)
    reservas = response.json()
    return render(request, 'reservas/reserva_api.html', {'reservas_mostrar':reservas})
        


def usuarios_lista_api(request):
    headers = {'Authorization': 'Bearer ' + env('OAUTH2_ACCESS_TOKEN_PROVEEDOR')} 
    response = requests.get('http://alvaroconde.pythonanywhere.com/api/v1/usuarios', headers=headers)
    usuarios = response.json()
    return render(request, 'usuarios/usuario_api.html', {'usuarios_mostrar': usuarios})



def reservasMejoradas_lista_api(request):
    headers = {'Authorization': 'Bearer ' + env('OAUTH2_ACCESS_TOKEN_CLIENTE')} 
    response = requests.get('http://alvaroconde.pythonanywhere.com/api/v1/reservasMejoradas', headers=headers)
    reservas = response.json()
    return render(request, 'reservas/reservaMejorada_api.html', {'reservas_mostrar': reservas})



def alojamientosMejorados_lista_api(request):
    headers = {'Authorization': 'Bearer ' + env('OAUTH2_ACCESS_TOKEN_ADMIN')} 
    response = requests.get('http://alvaroconde.pythonanywhere.com/api/v1/alojamientosMejorados', headers=headers)
    alojamientos = response.json()
    return render(request, 'alojamientos/alojamientoMejorado_api.html', {'alojamientos_mostrar': alojamientos})



def transportesMejorados_lista_api(request):
    headers = {'Authorization': 'Bearer ' + env('OAUTH2_ACCESS_TOKEN_CLIENTE')} 
    response = requests.get('http://alvaroconde.pythonanywhere.com/api/v1/transportesMejorados', headers=headers)
    transportes = response.json()
    return render(request, 'transportes/transporteMejorado_api.html', {'transportes_mostrar': transportes})



def reserva_busqueda_simple(request):
    formulario = BusquedaReservaForm(request.GET)

    if formulario.is_valid():
        headers = crear_cabecera()  
        response = requests.get(
            'http://0.0.0.0:8000/api/v1/reservas/busqueda_simple',
            headers=headers,
            params={'textoBusqueda': formulario.data.get("textoBusqueda")}
        )
        reservas = response.json()
        return render(request, 'reservas/lista_reservas.html', {"reservas_mostrar": reservas})

    # Redirigir si el formulario no es válido
    if "HTTP_REFERER" in request.META:
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("principal")
    
    
    
def reserva_busqueda_avanzada(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaReservaForm(request.GET)
        
        if formulario.is_valid():
            try:
                # Crear cabeceras necesarias para la petición (puedes adaptarlas según sea necesario)
                headers = crear_cabecera()
                
                # Realizar la solicitud GET a la API
                response = requests.get(
                    'http://0.0.0.0:8000/api/v1/reservas/busqueda_avanzada',  # URL de la API de búsqueda avanzada de reservas
                    headers=headers,
                    params=formulario.cleaned_data  # Pasar los datos del formulario validados
                )
                
                if response.status_code == requests.codes.ok:
                    reservas = response.json()  # Obtener las reservas de la respuesta JSON
                    return render(request, 'reservas/busqueda_avanzada.html', {"formulario": formulario,"reservas_mostrar": reservas})
                else:
                    print(response.status_code)
                    response.raise_for_status()
            except HTTPError as http_err:
                print(f'Hubo un error en la petición: {http_err}')
                if response.status_code == 400:
                    errores = response.json()
                    for error in errores:
                        formulario.add_error(error, errores[error])  # Agregar los errores del formulario
                    return render(request, 'reservas/busqueda_avanzada.html', {"formulario": formulario, "errores": errores})
                else:
                    return mi_error_500(request)  # Retornar una página de error 500
            except Exception as err:
                print(f'Ocurrió un error: {err}')
                return mi_error_500(request)
        else:
            # Si el formulario no es válido, redirige con los errores
            return render(request, 'reservas/busqueda_avanzada.html', {"formulario": formulario})
    else:
        formulario = BusquedaAvanzadaReservaForm(None)
        
    return render(request, 'reservas/busqueda_avanzada.html', {"formulario": formulario})


def usuario_busqueda_avanzada(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaUsuarioForm(request.GET)
        
        if formulario.is_valid():
            try:
                # Crear cabeceras necesarias para la petición (puedes adaptarlas según sea necesario)
                headers = crear_cabecera()
                
                # Realizar la solicitud GET a la API
                response = requests.get(
                    'http://0.0.0.0:8000/api/v1/usuarios/busqueda_avanzada',  # URL de la API de búsqueda avanzada de reservas
                    headers=headers,
                    params=formulario.cleaned_data  # Pasar los datos del formulario validados
                )
                
                if response.status_code == requests.codes.ok:
                    usuarios = response.json()  # Obtener las usuarios de la respuesta JSON
                    return render(request, 'usuarios/busqueda_avanzada.html', {"formulario": formulario, "usuarios_mostrar": usuarios})
                else:
                    print(response.status_code)
                    response.raise_for_status()
            except HTTPError as http_err:
                print(f'Hubo un error en la petición: {http_err}')
                if response.status_code == 400:
                    errores = response.json()
                    for error in errores:
                        formulario.add_error(error, errores[error])  # Agregar los errores del formulario
                    return render(request, 'usuarios/busqueda_avanzada.html', {"formulario": formulario, "errores": errores})
                else:
                    return mi_error_500(request)  # Retornar una página de error 500
            except Exception as err:
                print(f'Ocurrió un error: {err}')
                return mi_error_500(request)
        else:
            # Si el formulario no es válido, redirige con los errores
            return render(request, 'usuarios/busqueda_avanzada.html', {"formulario": formulario})
    else:
        formulario = BusquedaAvanzadaUsuarioForm(None)
        
    return render(request, 'usuarios/busqueda_avanzada.html', {"formulario": formulario})


def destino_busqueda_avanzada(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaDestinoForm(request.GET)
        
        if formulario.is_valid():
            try:
                # Crear cabeceras necesarias para la petición (puedes adaptarlas según sea necesario)
                headers = crear_cabecera()
                
                # Realizar la solicitud GET a la API
                response = requests.get(
                    'http://0.0.0.0:8000/api/v1/destinos/busqueda_avanzada',  # URL de la API de búsqueda avanzada de reservas
                    headers=headers,
                    params=formulario.cleaned_data  # Pasar los datos del formulario validados
                )
                
                if response.status_code == requests.codes.ok:
                    destinos = response.json()  # Obtener las destinos de la respuesta JSON
                    return render(request, 'destinos/busqueda_avanzada.html', {"formulario": formulario, "destinos_mostrar": destinos})
                else:
                    print(response.status_code)
                    response.raise_for_status()
            except HTTPError as http_err:
                print(f'Hubo un error en la petición: {http_err}')
                if response.status_code == 400:
                    errores = response.json()
                    for error in errores:
                        formulario.add_error(error, errores[error])  # Agregar los errores del formulario
                    return render(request, 'destinos/busqueda_avanzada.html', {"formulario": formulario, "errores": errores})
                else:
                    return mi_error_500(request)  # Retornar una página de error 500
            except Exception as err:
                print(f'Ocurrió un error: {err}')
                return mi_error_500(request)
        else:
            # Si el formulario no es válido, redirige con los errores
            return render(request, 'destinos/busqueda_avanzada.html', {"formulario": formulario})
    else:
        formulario = BusquedaAvanzadaDestinoForm(None)
        
    return render(request, 'destinos/busqueda_avanzada.html', {"formulario": formulario})


def comentario_busqueda_avanzada(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaComentarioForm(request.GET)
        
        if formulario.is_valid():
            try:
                # Crear cabeceras necesarias para la petición (puedes adaptarlas según sea necesario)
                headers = crear_cabecera()
                
                # Realizar la solicitud GET a la API
                response = requests.get(
                    'http://0.0.0.0:8000/api/v1/comentarios/busqueda_avanzada',  # URL de la API de búsqueda avanzada de reservas
                    headers=headers,
                    params=formulario.cleaned_data  # Pasar los datos del formulario validados
                )
                
                if response.status_code == requests.codes.ok:
                    comentarios = response.json()  # Obtener las destinos de la respuesta JSON
                    return render(request, 'comentarios/busqueda_avanzada.html', {"formulario": formulario, "comentarios_mostrar": comentarios})
                else:
                    print(response.status_code)
                    response.raise_for_status()
            except HTTPError as http_err:
                print(f'Hubo un error en la petición: {http_err}')
                if response.status_code == 400:
                    errores = response.json()
                    for error in errores:
                        formulario.add_error(error, errores[error])  # Agregar los errores del formulario
                    return render(request, 'comentarios/busqueda_avanzada.html', {"formulario": formulario, "errores": errores})
                else:
                    return mi_error_500(request)  # Retornar una página de error 500
            except Exception as err:
                print(f'Ocurrió un error: {err}')
                return mi_error_500(request)
        else:
            # Si el formulario no es válido, redirige con los errores
            return render(request, 'comentarios/busqueda_avanzada.html', {"formulario": formulario})
    else:
        formulario = BusquedaAvanzadaComentarioForm(None)
        
    return render(request, 'comentarios/busqueda_avanzada.html', {"formulario": formulario})





#Páginas de Error
def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

#Páginas de Error
def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)
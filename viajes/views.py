from requests.exceptions import HTTPError
from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Q, Sum
from django.contrib import messages
from django.contrib.auth.models import Group
import requests
from datetime import datetime

from django.conf import settings
import environ
import os
from pathlib import Path
from .forms import *
import xml.etree.ElementTree as ET
import json
from .helper import helper


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


# Definir una constante para la base de la URL de la API.
# Esto permite cambiar la versión de la API en un solo lugar si es necesario en el futuro.
API_BASE_URL = "http://0.0.0.0:8000/api/v1/"

# alvaroconde.pythonanywhere.com


# En lugar de usar siempre response.json(), creamos una función que detecta 
# automáticamente si la API responde con JSON o XML. Así evitamos tener que 
# cambiar manualmente todas las líneas en el futuro si cambia el formato.

def procesar_respuesta(response):
    """Detecta y procesa la respuesta según su formato (JSON o XML)."""
    content_type = response.headers.get('Content-Type', '')

    if 'application/json' in content_type:
        return response.json()  # Procesar JSON
    elif 'application/xml' in content_type or 'text/xml' in content_type:
        return ET.fromstring(response.text)  # Procesar XML
    else:
        raise ValueError("Formato de respuesta desconocido")


#######################################################################################################################################################################


def reservas_lista_api(request):
    headers = {'Authorization' : 'Bearer '+env('OAUTH2_ACCESS_TOKEN_ADMIN')}    
    response = requests.get(API_BASE_URL + 'reservas', headers=headers)
    reservas = response.json()
    return render(request, 'reservas/reserva_api.html', {'reservas_mostrar':reservas})
        


def usuarios_lista_api(request):
    headers = {'Authorization': 'Bearer ' + env('OAUTH2_ACCESS_TOKEN_PROVEEDOR')} 
    response = requests.get(API_BASE_URL + 'usuarios', headers=headers)
    usuarios = response.json()
    return render(request, 'usuarios/usuario_api.html', {'usuarios_mostrar': usuarios})



def reservasMejoradas_lista_api(request):
    headers = {'Authorization': 'Bearer ' + env('OAUTH2_ACCESS_TOKEN_CLIENTE')} 
    response = requests.get(API_BASE_URL + 'reservasMejoradas', headers=headers)
    reservas = response.json()
    return render(request, 'reservas/reservaMejorada_api.html', {'reservas_mostrar': reservas})



def alojamientosMejorados_lista_api(request):
    headers = {'Authorization': 'Bearer ' + env('OAUTH2_ACCESS_TOKEN_ADMIN')} 
    response = requests.get(API_BASE_URL + 'alojamientosMejorados', headers=headers)
    alojamientos = response.json()
    return render(request, 'alojamientos/alojamientoMejorado_api.html', {'alojamientos_mostrar': alojamientos})



def transportesMejorados_lista_api(request):
    headers = {'Authorization': 'Bearer ' + env('OAUTH2_ACCESS_TOKEN_CLIENTE')} 
    response = requests.get(API_BASE_URL + 'transportesMejorados', headers=headers)
    transportes = response.json()
    return render(request, 'transportes/transporteMejorado_api.html', {'transportes_mostrar': transportes})


#######################################################################################################################################################################


def reserva_busqueda_simple(request):
    formulario = BusquedaReservaForm(request.GET)

    if formulario.is_valid():
        headers = crear_cabecera()  
        response = requests.get(
            API_BASE_URL + 'reservas/busqueda_simple',
            headers=headers,
            params={'textoBusqueda': formulario.data.get("textoBusqueda")}
        )
        reservas = procesar_respuesta(response)
        return render(request, 'reservas/lista_reservas.html', {"reservas_mostrar": reservas})

    # Redirigir si el formulario no es válido
    if "HTTP_REFERER" in request.META:
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("principal")
    
    
    
def reserva_busqueda_avanzada(request):
    errores = None  # Variable para capturar errores

    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaReservaForm(request.GET)
        
        if formulario.is_valid():
            try:
                # Crear cabeceras necesarias para la petición (puedes adaptarlas según sea necesario)
                headers = crear_cabecera()
                
                # Realizar la solicitud GET a la API
                response = requests.get(
                    API_BASE_URL +'reservas/busqueda_avanzada',  # URL de la API de búsqueda avanzada de reservas
                    headers=headers,
                    params=formulario.cleaned_data  # Pasar los datos del formulario validados
                )
                
                if response.status_code == requests.codes.ok:
                    reservas = procesar_respuesta(response)  # Obtener las reservas de la respuesta JSON
                    return render(request, 'reservas/busqueda_avanzada.html', {"formulario": formulario,"reservas_mostrar": reservas, "errores": errores})
                else:
                    print(response.status_code)
                    response.raise_for_status()
            
            except HTTPError as http_err:
                print(f'Hubo un error en la petición: {http_err}')
                if response.status_code == 400:
                    errores = procesar_respuesta(response)
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
        
    return render(request, 'reservas/busqueda_avanzada.html', {"formulario": formulario, "errores": errores})


def usuario_busqueda_avanzada(request):
    errores = None  # Variable para capturar errores

    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaUsuarioForm(request.GET)
        
        if formulario.is_valid():
            try:
                # Crear cabeceras necesarias para la petición (puedes adaptarlas según sea necesario)
                headers = crear_cabecera()
                
                # Realizar la solicitud GET a la API
                response = requests.get(
                    API_BASE_URL + 'usuarios/busqueda_avanzada',  # URL de la API de búsqueda avanzada de reservas
                    headers=headers,
                    params=formulario.cleaned_data  # Pasar los datos del formulario validados
                )
                
                if response.status_code == requests.codes.ok:
                    usuarios = procesar_respuesta(response)  # Obtener las usuarios de la respuesta JSON
                    return render(request, 'usuarios/busqueda_avanzada.html', {"formulario": formulario, "usuarios_mostrar": usuarios, "errores": errores})
                else:
                    print(response.status_code)
                    response.raise_for_status()
            
            except HTTPError as http_err:
                print(f'Hubo un error en la petición: {http_err}')
                if response.status_code == 400:
                    errores = procesar_respuesta(response)
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
        
    return render(request, 'usuarios/busqueda_avanzada.html', {"formulario": formulario, "errores": errores})


def destino_busqueda_avanzada(request):
    errores = None  # Variable para capturar errores

    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaDestinoForm(request.GET)
        
        if formulario.is_valid():
            try:
                # Crear cabeceras necesarias para la petición (puedes adaptarlas según sea necesario)
                headers = crear_cabecera()
                
                # Realizar la solicitud GET a la API
                response = requests.get(
                    API_BASE_URL + 'destinos/busqueda_avanzada',  # URL de la API de búsqueda avanzada de reservas
                    headers=headers,
                    params=formulario.cleaned_data  # Pasar los datos del formulario validados
                )
                
                if response.status_code == requests.codes.ok:
                    destinos = procesar_respuesta(response)  # Obtener las destinos de la respuesta JSON
                    return render(request, 'destinos/busqueda_avanzada.html', {"formulario": formulario, "destinos_mostrar": destinos, "errores": errores})
                else:
                    print(response.status_code)
                    response.raise_for_status()
            
            except HTTPError as http_err:
                print(f'Hubo un error en la petición: {http_err}')
                if response.status_code == 400:
                    errores = procesar_respuesta(response)
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
        
    return render(request, 'destinos/busqueda_avanzada.html', {"formulario": formulario, "errores": errores})


def comentario_busqueda_avanzada(request):
    errores = None  # Variable para capturar errores

    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaComentarioForm(request.GET)
        
        if formulario.is_valid():
            try:
                # Crear cabeceras necesarias para la petición (puedes adaptarlas según sea necesario)
                headers = crear_cabecera()
                
                # Realizar la solicitud GET a la API
                response = requests.get(
                    API_BASE_URL + 'comentarios/busqueda_avanzada',  # URL de la API de búsqueda avanzada de reservas
                    headers=headers,
                    params=formulario.cleaned_data  # Pasar los datos del formulario validados
                )
                
                if response.status_code == requests.codes.ok:
                    comentarios = procesar_respuesta(response)  # Obtener las comentarios de la respuesta JSON
                    return render(request, 'comentarios/busqueda_avanzada.html', {"formulario": formulario, "comentarios_mostrar": comentarios, "errores": errores})
                else:
                    print(response.status_code)
                    response.raise_for_status()
            
            except HTTPError as http_err:
                print(f'Hubo un error en la petición: {http_err}')
                if response.status_code == 400:
                    errores = procesar_respuesta(response)
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
        
    return render(request, 'comentarios/busqueda_avanzada.html', {"formulario": formulario, "errores": errores})


def alojamiento_busqueda_avanzada(request):
    errores = None  # Variable para capturar errores

    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaAlojamientoForm(request.GET)
        
        if formulario.is_valid():
            try:
                # Crear cabeceras necesarias para la petición (puedes adaptarlas según sea necesario)
                headers = crear_cabecera()
                
                # Realizar la solicitud GET a la API
                response = requests.get(
                    API_BASE_URL + 'alojamientos/busqueda_avanzada',  # URL de la API de búsqueda avanzada de reservas
                    headers=headers,
                    params=formulario.cleaned_data  # Pasar los datos del formulario validados
                )
                
                if response.status_code == requests.codes.ok:
                    alojamientos = procesar_respuesta(response)  # Obtener las destinos de la respuesta JSON
                    return render(request, 'alojamientos/busqueda_avanzada.html', {"formulario": formulario, "alojamientos_mostrar": alojamientos, "errores": errores})
                else:
                    print(response.status_code)
                    response.raise_for_status()

            except HTTPError as http_err:
                print(f'Hubo un error en la petición: {http_err}')
                if response.status_code == 400:
                    errores = procesar_respuesta(response)
                    for error in errores:
                        formulario.add_error(error, errores[error])  # Agregar los errores del formulario
                    return render(request, 'alojamientos/busqueda_avanzada.html', {"formulario": formulario, "errores": errores})
                else:
                    return mi_error_500(request)  # Retornar una página de error 500
            
            except Exception as err:
                print(f'Ocurrió un error: {err}')
                return mi_error_500(request)
        else:
            # Si el formulario no es válido, redirige con los errores
            return render(request, 'alojamientos/busqueda_avanzada.html', {"formulario": formulario})
    else:
        formulario = BusquedaAvanzadaAlojamientoForm(None)
        
    return render(request, 'alojamientos/busqueda_avanzada.html', {"formulario": formulario, "errores": errores})


#######################################################################################################################################################################


def reserva_crear(request):
    if request.method == "POST":
        try:
            formulario = ReservaForm(request.POST)
            headers = crear_cabecera()
            datos = formulario.data.copy()
            
            datos["fecha_salida"] = str(datetime.strptime(datos["fecha_salida"], "%Y-%m-%d").date())
            datos["fecha_llegada"] = str(datetime.strptime(datos["fecha_llegada"], "%Y-%m-%d").date())
            
            response = requests.post(
                'http://0.0.0.0:8000/api/v1/reservas/crear',
                headers=headers,
                data=json.dumps(datos)
            )
            
            if response.status_code == requests.codes.ok:
                return redirect("reservas_lista_api")
            else:
                print(response.status_code)
                response.raise_for_status()
                
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if (response.status_code == 400):
                errores = response.json()
                
                for error in errores:
                    formulario.add_error(error, errores[error])
                
                return render(request, 'reservas/create.html', {"formulario": formulario})
            else:
                return mi_error_500(request)
            
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
        
    else:
        formulario = ReservaForm(None)
    
    return render(request, 'reservas/create.html', {"formulario": formulario})



def usuario_crear(request):
    if request.method == "POST":
        try:
            formulario = UsuarioForm(request.POST, request.FILES)  # Para incluir los archivos (imagen)
            headers = crear_cabecera() 
            datos = formulario.data.copy()

            if datos.get("fecha_registro"):
                datos["fecha_registro"] = str(datetime.strptime(datos["fecha_registro"], "%Y-%m-%d").date())
            
            response = requests.post(
                'http://0.0.0.0:8000/api/v1/usuarios/crear',  
                headers=headers,
                data=json.dumps(datos),  # Convertimos los datos a JSON
                files=request.FILES  # Enviamos los archivos (imagen de perfil)
            )

            if response.status_code == requests.codes.ok:  
                return redirect("usuarios_lista_api")  
            else:
                print(response.status_code)
                response.raise_for_status()

        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if response.status_code == 400:  # Si hay un error 400, mostramos los errores del formulario
                errores = response.json()
                for error in errores:
                    formulario.add_error(error, errores[error])

                return render(request, 'usuarios/create.html', {"formulario": formulario})
            else:
                return mi_error_500(request)  # Manejamos el error genérico si no es 400

        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)  # Manejamos cualquier otro error genérico

    else:
        formulario = UsuarioForm()  # Si no es POST, mostramos el formulario vacío

    return render(request, 'usuarios/create.html', {"formulario": formulario})


def transporte_crear(request):
    if request.method == "POST":
        try:
            formulario = TransporteForm(request.POST)  # Para incluir los datos del formulario
            headers = crear_cabecera()  # Si es necesario añadir alguna cabecera
            datos = formulario.data.copy()


            # Asegúrate de que el campo 'destino' sea una lista de valores seleccionados
            datos["destino"] = request.POST.getlist("destino")  # Asignamos la lista de destinos al campo 'destino'


            # Realiza la solicitud POST al API
            response = requests.post(
                'http://0.0.0.0:8000/api/v1/transportes/crear',  # URL para crear transporte
                headers=headers,
                data=json.dumps(datos),  # Convertimos los datos del formulario a JSON
            )

            # Verifica si la respuesta fue exitosa
            if response.status_code == 201:
                return redirect("transportesMejorados_lista_api")  # Redirige a la lista de transportes
            else:
                print(response.status_code)
                response.raise_for_status()

        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if response.status_code == 400:  # Si hay errores de validación
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 'transportes/create.html', {"formulario": formulario})
            else:
                return mi_error_500(request)  # Manejo de errores internos

        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)

    else:
        formulario = TransporteForm()  # Si no es POST, muestra un formulario vacío

    return render(request, 'transportes/create.html', {"formulario": formulario})


#######################################################################################################################################################################


from .cliente_api import cliente_api

from datetime import datetime
from decimal import Decimal

def reserva_editar(request, reserva_id):
    datosFormulario = None
    
    # Si el método es POST, obtenemos los datos del formulario
    if request.method == "POST":
        datosFormulario = request.POST
    
    # Obtener los datos de la reserva desde el helper
    reserva = helper.obtener_reserva(reserva_id)
    
    # Crear un formulario con los datos iniciales
    formulario = ReservaForm(
        datosFormulario,
        initial={
            'codigo_reserva': reserva['codigo_reserva'],
            'fecha_salida': datetime.strptime(reserva['fecha_salida'], '%d-%m-%Y').date(),
            'fecha_llegada': datetime.strptime(reserva['fecha_llegada'], '%d-%m-%Y').date(),
            'numero_personas': reserva['numero_personas'],
            'precio': float(reserva['precio']) if isinstance(reserva['precio'], Decimal) else reserva['precio']  # Convierte Decimal a float
        }
    )
    
    # Si el formulario es enviado con método POST y es válido
    if request.method == "POST" and formulario.is_valid():
        datos = formulario.cleaned_data.copy()
        datos["fecha_salida"] = datos["fecha_salida"].strftime('%Y-%m-%d')
        datos["fecha_llegada"] = datos["fecha_llegada"].strftime('%Y-%m-%d')

        # 🔹 Asegurar que el precio se convierta a float antes de enviarlo
        if isinstance(datos["precio"], Decimal):
            datos["precio"] = float(datos["precio"])

        cliente = cliente_api(env("OAUTH2_ACCESS_TOKEN"), "PUT", f'reservas/editar/{reserva_id}', datos)
        cliente.realizar_peticion_api()

        if cliente.es_respuesta_correcta():
            return redirect("reservas_lista_api")
        elif cliente.es_error_validacion_datos():
            cliente.incluir_errores_formulario(formulario)
        else:
            return tratar_errores(request, cliente.codigoRespuesta)
    
    return render(request, 'reservas/actualizar.html', {"formulario": formulario, "reserva": reserva})



def usuario_editar(request, usuario_id):
    datosFormulario = None

    # Si el método es POST, obtenemos los datos del formulario
    if request.method == "POST":
        datosFormulario = request.POST
    
    # Obtener los datos del usuario desde el helper
    usuario = helper.obtener_usuario(usuario_id)
    
    # Crear un formulario con los datos iniciales
    formulario = UsuarioForm(
        datosFormulario,
        initial={
            'nombre': usuario['nombre'],
            'correo': usuario['correo'],
            'telefono': usuario['telefono'],
            'edad': usuario['edad'],
            'contraseña': usuario['contraseña'],  # No es recomendable cargar contraseñas, podrías omitirlo
            'fecha_registro': datetime.strptime(usuario['fecha_registro'], '%Y-%m-%d').date(),
        }
    )
    
    # Si el formulario es enviado con método POST y es válido
    if request.method == "POST" and formulario.is_valid():
        datos = formulario.cleaned_data.copy()
        
        # Convertir la fecha a formato YYYY-MM-DD
        if datos["fecha_registro"]:
            datos["fecha_registro"] = datos["fecha_registro"].strftime('%Y-%m-%d')
        else:
            datos["fecha_registro"] = None

        # Hacer la petición API para actualizar usuario
        cliente = cliente_api(
            os.getenv("OAUTH2_ACCESS_TOKEN"), "PUT", f'usuarios/editar/{usuario_id}', datos
        )
        cliente.realizar_peticion_api()

        if cliente.es_respuesta_correcta():
            return redirect("usuarios_lista_api")
        elif cliente.es_error_validacion_datos():
            cliente.incluir_errores_formulario(formulario)
        else:
            return tratar_errores(request, cliente.codigoRespuesta)
    
    return render(request, 'usuarios/actualizar.html', {"formulario": formulario, "usuario": usuario})


#######################################################################################################################################################################


def reserva_actualizar_codigo(request, reserva_id):
    datosFormulario = None
    reserva = helper.obtener_reserva(reserva_id)  # Obtenemos los datos de la reserva

    formulario = ReservaActualizarCodigoForm(datosFormulario,
            initial={
                'codigo_reserva': reserva['codigo_reserva'],
            }
    )

    if request.method == "POST":
        try:
            formulario = ReservaActualizarCodigoForm(request.POST)
            headers = crear_cabecera()
            datos = request.POST.copy()
            response = requests.patch(
                API_BASE_URL + "reservas/actualizar/codigo/" + str(reserva_id),
                headers=headers,
                data=json.dumps(datos)
            )

            if response.status_code == requests.codes.ok:
                return redirect("reservas_lista_api")  # Redirige a la vista de mostrar la reserva
            else:
                print(response.status_code)
                response.raise_for_status()

        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if response.status_code == 400:
                errores = response.json()
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, 'reservas/actualizar_codigo.html', {"formulario": formulario, "reserva": reserva})
            else:
                return mi_error_500(request)  # Esta es una función para manejar errores internos

        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)

    return render(request, 'reservas/actualizar_codigo.html', {"formulario": formulario, "reserva": reserva})


def usuario_actualizar_nombre(request, usuario_id):
    datosFormulario = None
    usuario = helper.obtener_usuario(usuario_id)  # Obtenemos los datos del usuario

    formulario = UsuarioActualizarNombreForm(datosFormulario,
            initial={
                'nombre': usuario['nombre'],  # Solo el campo 'nombre' será editable
            }
    )

    if request.method == "POST":
        try:
            formulario = UsuarioActualizarNombreForm(request.POST)  # Volvemos a instanciar el formulario con los datos POST
            headers = crear_cabecera()  # Función que genera las cabeceras necesarias (token de autenticación, etc.)
            datos = request.POST.copy()  # Copiamos los datos del formulario

            # Realizamos el PATCH a la API para actualizar el nombre
            response = requests.patch(
                API_BASE_URL + "usuarios/actualizar/nombre/" + str(usuario_id),  # Endpoint para actualizar el nombre del usuario
                headers=headers,
                data=json.dumps(datos)  # Enviamos los datos como JSON
            )

            if response.status_code == requests.codes.ok:  # Si la respuesta es exitosa
                return redirect("usuarios_lista_api")  # Redirige a la vista de la lista de usuarios
            else:
                print(response.status_code)
                response.raise_for_status()

        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if response.status_code == 400:  # Si hay un error de validación
                errores = response.json()
                for error in errores:
                    formulario.add_error(error, errores[error])  # Añadimos los errores al formulario
                return render(request, 'usuarios/actualizar_nombre.html', {"formulario": formulario, "usuario": usuario})
            else:
                return mi_error_500(request)  # Manejo de errores internos

        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)  # Manejo general de errores

    return render(request, 'usuarios/actualizar_nombre.html', {"formulario": formulario, "usuario": usuario})


#######################################################################################################################################################################


def reserva_eliminar(request, reserva_id):
    try:
        headers = crear_cabecera()
        response = requests.delete(
            API_BASE_URL + "reservas/eliminar/" + str(reserva_id),
            headers=headers,
        )
        if response.status_code == requests.codes.ok:
            return redirect("reservas_lista_api")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    
    return redirect("reservas_lista_api")


def usuario_eliminar(request, usuario_id):
    try:
        headers = crear_cabecera()
        response = requests.delete(
            API_BASE_URL + "usuarios/eliminar/" + str(usuario_id),
            headers=headers,
        )
        if response.status_code == requests.codes.ok:
            return redirect("usuarios_lista_api")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    
    return redirect("usuarios_lista_api")


#######################################################################################################################################################################


def tratar_errores(request,codigo):
    if codigo == 404:
        return mi_error_404(request)
    else:
        return mi_error_500(request)


#Páginas de Error
def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

#Páginas de Error
def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)
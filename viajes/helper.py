import requests
import environ
import os
from pathlib import Path
from requests.exceptions import HTTPError
import json

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'), True)
env = environ.Env()

class helper:

    def crear_cabecera():
        return {
            "Authorization": "Bearer " + env("OAUTH2_ACCESS_TOKEN"),
            "Content-Type": "application/json"
        }
    

#######################################################################################################################################################################


    def crear_reserva(datos):
        headers = helper.crear_cabecera()

        try:
            response = requests.post(
                'http://0.0.0.0:8000/api/v1/reservas/crear',
                headers=headers,
                data=json.dumps(datos)
            )

            response.raise_for_status()  # Levanta una excepción si la respuesta es un error HTTP
            return response

        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            return response  # Devuelve la respuesta para manejar el error en la vista

        except Exception as err:
            print(f'Ocurrió un error inesperado: {err}')
            return None  # Retorna None en caso de error crítico
        

    def crear_usuario(datos, archivos):
        headers = helper.crear_cabecera()

        try:
            response = requests.post(
                'http://0.0.0.0:8000/api/v1/usuarios/crear',
                headers=headers,
                data=json.dumps(datos),  # Convertimos los datos a JSON
                files=archivos  # Enviamos archivos (como imagen de perfil)
            )

            response.raise_for_status()  # Levanta una excepción si la respuesta es un error HTTP
            return response

        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            return response  # Devuelve la respuesta para manejar el error en la vista

        except Exception as err:
            print(f'Ocurrió un error inesperado: {err}')
            return None  # Retorna None en caso de error crítico
        

    def crear_transporte(datos):
        headers = helper.crear_cabecera()

        try:
            response = requests.post(
                'http://0.0.0.0:8000/api/v1/transportes/crear',
                headers=headers,
                data=json.dumps(datos),  # Convertimos los datos a JSON
            )

            response.raise_for_status()  # Levanta una excepción si la respuesta es un error HTTP
            return response

        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            return response  # Devuelve la respuesta para manejar el error en la vista

        except Exception as err:
            print(f'Ocurrió un error inesperado: {err}')
            return None  # Retorna None en caso de error crítico
        

    def crear_extra(datos):
        headers = helper.crear_cabecera()

        try:
            response = requests.post(
                'http://0.0.0.0:8000/api/v1/extras/crear',
                headers=headers,
                data=json.dumps(datos),  # Convertimos los datos a JSON
            )

            response.raise_for_status()  # Levanta una excepción si la respuesta es un error HTTP
            return response

        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            return response  # Devuelve la respuesta para manejar el error en la vista

        except Exception as err:
            print(f'Ocurrió un error inesperado: {err}')
            return None  # Retorna None en caso de error crítico


#######################################################################################################################################################################


    def editar_reserva(reserva_id, datos):
        headers = {'Authorization': 'Bearer ' + env("OAUTH2_ACCESS_TOKEN"), "Content-Type": "application/json"}

        try:
            response = requests.put(
                f'http://0.0.0.0:8000/api/v1/reservas/editar/{reserva_id}',
                headers=headers,
                data=json.dumps(datos),
            )

            response.raise_for_status()  # Levanta una excepción si hay un error HTTP
            return response

        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            return response  # Devuelve la respuesta para manejar el error en la vista

        except Exception as err:
            print(f'Ocurrió un error inesperado: {err}')
            return None  # Retorna None en caso de error crítico
        

    def editar_usuario(usuario_id, datos):
        headers = {'Authorization': 'Bearer ' + env("OAUTH2_ACCESS_TOKEN"), "Content-Type": "application/json"}

        try:
            response = requests.put(
                f'http://0.0.0.0:8000/api/v1/usuarios/editar/{usuario_id}',
                headers=headers,
                data=json.dumps(datos),
            )

            response.raise_for_status()  # Levanta una excepción si hay un error HTTP
            return response

        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            return response  # Devuelve la respuesta para manejar el error en la vista

        except Exception as err:
            print(f'Ocurrió un error inesperado: {err}')
            return None  # Retorna None en caso de error crítico
        

    def editar_transporte(transporte_id, datos):
        headers = {'Authorization': 'Bearer ' + env("OAUTH2_ACCESS_TOKEN"), "Content-Type": "application/json"}

        try:
            response = requests.put(
                f'http://0.0.0.0:8000/api/v1/transportes/editar/{transporte_id}',
                headers=headers,
                data=json.dumps(datos),
            )

            response.raise_for_status()  # Levanta una excepción si hay un error HTTP
            return response

        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            return response  # Devuelve la respuesta para manejar el error en la vista

        except Exception as err:
            print(f'Ocurrió un error inesperado: {err}')
            return None  # Retorna None en caso de error crítico
        

    def editar_extra(extra_id, datos):
        headers = {'Authorization': 'Bearer ' + env("OAUTH2_ACCESS_TOKEN"), "Content-Type": "application/json"}

        try:
            response = requests.put(
                f'http://0.0.0.0:8000/api/v1/extras/editar/{extra_id}',
                headers=headers,
                data=json.dumps(datos),
            )

            response.raise_for_status()  # Levanta una excepción si hay un error HTTP
            return response

        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            return response  # Devuelve la respuesta para manejar el error en la vista

        except Exception as err:
            print(f'Ocurrió un error inesperado: {err}')
            return None  # Retorna None en caso de error crítico


#######################################################################################################################################################################


    def actualizar_codigo_reserva(reserva_id, datos):
        headers = {'Authorization': 'Bearer ' + env("OAUTH2_ACCESS_TOKEN"), "Content-Type": "application/json"}

        try:
            response = requests.patch(
                f'http://0.0.0.0:8000/api/v1/reservas/actualizar/codigo/{reserva_id}',
                headers=headers,
                data=json.dumps(datos),
            )

            response.raise_for_status()  # Levanta una excepción si hay un error HTTP
            return response

        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            return response  # Devuelve la respuesta para manejar el error en la vista

        except Exception as err:
            print(f'Ocurrió un error inesperado: {err}')
            return None  # Retorna None en caso de error crítico


#######################################################################################################################################################################

    
    def obtener_usuarios_select():
        headers = {'Authorization': 'Bearer ' + env("OAUTH2_ACCESS_TOKEN")}
        response = requests.get('http://0.0.0.0:8000/api/v1/usuarios', headers=headers)
        print(response.json)
        usuarios = response.json()

        lista_usuarios = []
        for usuario in usuarios:
            lista_usuarios.append((usuario["id"], usuario["nombre"]))
        return lista_usuarios
 
 
    def obtener_reserva(id):
        headers = {'Authorization': 'Bearer '+env("OAUTH2_ACCESS_TOKEN")} 
        response = requests.get('http://0.0.0.0:8000/api/v1/reservas/'+str(id), headers=headers)
        reserva = response.json()
        return reserva
    

    def obtener_usuario(id):
        headers = {'Authorization': 'Bearer '+env("OAUTH2_ACCESS_TOKEN")} 
        response = requests.get('http://0.0.0.0:8000/api/v1/usuarios/'+str(id), headers=headers)
        usuario = response.json()
        return usuario
    
    
    # Helper para obtener destinos
    def obtener_destinos_select():
        headers = {'Authorization': 'Bearer ' + env("OAUTH2_ACCESS_TOKEN")}
        response = requests.get('http://0.0.0.0:8000/api/v1/destinos', headers=headers)
        destinos = response.json()

        lista_destinos = []
        for destino in destinos:
            lista_destinos.append((destino["id"], destino["nombre"]))  # Usamos el "id" como valor y el "nombre" como texto
        return lista_destinos
    

    def obtener_transporte(id):
        headers = {'Authorization': 'Bearer '+env("OAUTH2_ACCESS_TOKEN")} 
        response = requests.get('http://0.0.0.0:8000/api/v1/transportes/'+str(id), headers=headers)
        transporte = response.json()
        return transporte


    def obtener_tipos_extra():
        # Lista fija de tipos de extra (esto lo puedes personalizar si es necesario)
        tipos_extra = [
            ('actividad', 'Actividad'),
            ('guia', 'Guía Turístico'),
            ('transporte', 'Transporte Adicional'),
            ('comida', 'Comida Especial'),
            ('seguro', 'Seguro'),
        ]
        return tipos_extra
    

    def obtener_reservas_select():
        headers = {'Authorization': 'Bearer ' + env("OAUTH2_ACCESS_TOKEN")}
        response = requests.get('http://0.0.0.0:8000/api/v1/reservas', headers=headers)
        reservas = response.json()

        lista_reservas = []
        for reserva in reservas:
            lista_reservas.append((reserva["id"], reserva["codigo_reserva"]))  # Usamos el "id" como valor y el "codigo_reserva" como texto
        return lista_reservas
    

    def obtener_extra(id):
        headers = {'Authorization': 'Bearer '+env("OAUTH2_ACCESS_TOKEN")} 
        response = requests.get('http://0.0.0.0:8000/api/v1/extras/'+str(id), headers=headers)
        extra = response.json()
        return extra


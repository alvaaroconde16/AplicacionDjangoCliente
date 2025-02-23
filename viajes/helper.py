import requests
import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'), True)
env = environ.Env()

class helper:
    
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


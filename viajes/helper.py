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

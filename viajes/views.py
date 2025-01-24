from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Q, Sum
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
import requests

# Create your views here.
def index(request):
    
    return render(request, 'principal.html')


def reservas_lista_api(request):
    response = requests.get('http://127.0.0.1:8000/api/v1/reservas')
    reservas = response.json()
    return render(request, 'reservas/reserva_api.html', {'reservas_mostrar':reservas})
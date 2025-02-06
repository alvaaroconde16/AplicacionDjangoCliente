from django import forms
from datetime import datetime, date

class BusquedaReservaForm(forms.Form):
    textoBusqueda = forms.CharField(required=False, label="Buscar Reserva")
    

class BusquedaAvanzadaReservaForm(forms.Form):
    
    # Campo de búsqueda por código de reserva (sin validación de longitud mínima)
    codigo_reserva = forms.CharField(required=False, label="Código de Reserva")

    # Campo de búsqueda por número de personas
    numero_personas = forms.IntegerField(required=False, label="Número de Personas", min_value=1)
    
    # Campo de búsqueda por nombre de usuario
    nombre_usuario = forms.CharField(required=False, label="Nombre de Usuario")

    
    # Campo de búsqueda por fecha
    fechaHoy = date.today().year
    fecha = forms.DateField(required=False, label="Fecha de la Reserva", widget=forms.DateInput(attrs={'type': 'date'}))
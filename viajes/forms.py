from django import forms
from datetime import datetime

class BusquedaReservaForm(forms.Form):
    textoBusqueda = forms.CharField(required=False, label="Buscar Reserva")
    

class BusquedaAvanzadaReservaForm(forms.Form):
    
    # Campo de búsqueda por código de reserva
    codigo_reserva = forms.CharField(required=False, label="Código de Reserva")
    
    # Campo de búsqueda por nombre de usuario (opcional)
    nombre_usuario = forms.CharField(required=False, label="Nombre del Usuario")

    # Campo de búsqueda por número de personas
    numero_personas = forms.IntegerField(required=False, label="Número de Personas", min_value=1)

    # Campo para elegir el rango de fechas
    fecha_desde = forms.DateField(
        label="Fecha Desde",
        required=False,
        widget=forms.SelectDateWidget(years=range(1990, 2025))
    )
    
    fecha_hasta = forms.DateField(
        label="Fecha Hasta",
        required=False,
        widget=forms.SelectDateWidget(years=range(1990, 2025))
    )

    # Campo de búsqueda por precio desde
    precio_desde = forms.DecimalField(
        required=False, 
        label="Precio Desde",
        max_digits=10, 
        decimal_places=2
    )
    
    # Campo de búsqueda por precio hasta
    precio_hasta = forms.DecimalField(
        required=False, 
        label="Precio Hasta", 
        max_digits=10, 
        decimal_places=2
    )
    

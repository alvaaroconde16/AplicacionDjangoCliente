from django import forms
from datetime import datetime

class BusquedaReservaForm(forms.Form):
    textoBusqueda = forms.CharField(required=False, label="Buscar Reserva")
    

class BusquedaAvanzadaReservaForm(forms.Form):
    codigo_reserva = forms.CharField(required=False, label="Código de Reserva")
    nombre_usuario = forms.CharField(required=False, label="Nombre del Usuario")

    # Campo para la fecha
    fecha_salida = forms.DateField(required=False, label="Fecha de Salida", 
                                   widget=forms.SelectDateWidget(years=range(1990, 2025)))

    fecha_llegada = forms.DateField(required=False, label="Fecha de Llegada", 
                                    widget=forms.SelectDateWidget(years=range(1990, 2025)))

    numero_personas = forms.IntegerField(required=False, label="Número de Personas", min_value=1)

    # Campo para precio de reserva
    precio_desde = forms.DecimalField(required=False, label="Precio Desde", 
                                      max_digits=10, decimal_places=2)
    
    precio_hasta = forms.DecimalField(required=False, label="Precio Hasta", 
                                      max_digits=10, decimal_places=2)
    
    # Rango de fechas desde
    current_year = datetime.now().year 
    
    fecha_desde = forms.DateField(
        required=False,
        label="Fecha Desde",
        widget=forms.SelectDateWidget(years=range(1990, current_year + 1))
    )
    
    # Rango de fechas hasta
    fecha_hasta = forms.DateField(
        required=False,
        label="Fecha Hasta",
        widget=forms.SelectDateWidget(years=range(1990, current_year + 1))
    )


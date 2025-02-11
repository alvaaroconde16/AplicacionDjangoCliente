from django import forms
from datetime import datetime, date
from .helper import helper

class BusquedaReservaForm(forms.Form):
    textoBusqueda = forms.CharField(required=False, label="Buscar Reserva")

    

class BusquedaAvanzadaReservaForm(forms.Form):
    
    # Campo de búsqueda por código de reserva (sin validación de longitud mínima)
    codigo_reserva = forms.CharField(required=False, label="Código de Reserva")

    # Campo de búsqueda por número de personas
    numero_personas = forms.IntegerField(required=False, label="Número de Personas")
    
    # Campo de búsqueda por fecha
    fechaHoy = date.today().year
    fecha = forms.DateField(required=False, label="Fecha de la Reserva", widget=forms.DateInput(attrs={'type': 'date'}))
    


class BusquedaAvanzadaUsuarioForm(forms.Form):
    # Campo de búsqueda por nombre
    nombre = forms.CharField(required=False, label="Nombre")

    # Campo de búsqueda por correo
    correo = forms.EmailField(required=False, label="Correo Electrónico")

    # Campo para edad
    edad = forms.IntegerField(required=False, label="Edad")
    
    

class BusquedaAvanzadaDestinoForm(forms.Form):
    # Campo de búsqueda por nombre del destino
    nombre = forms.CharField(required=False, label="Nombre del Destino")

    # Campo de búsqueda por país del destino
    pais = forms.CharField(required=False, label="País")

    # Campo de búsqueda por popularidad
    popularidad = forms.FloatField(required=False, label="Popularidad")
    
    
    
class BusquedaAvanzadaComentarioForm(forms.Form):
    # Campo de búsqueda por título del comentario
    titulo = forms.CharField(required=False, label="Título del Comentario")

    # Campo de búsqueda por contenido del comentario
    contenido = forms.CharField(required=False, label="Contenido")

    # Campo de búsqueda por calificación
    calificacion = forms.FloatField(required=False, label="Calificación",)



class BusquedaAvanzadaAlojamientoForm(forms.Form):
    # Campo de búsqueda por nombre de alojamiento
    nombre = forms.CharField(required=False, label="Nombre del Alojamiento")
    
    # Campo de búsqueda por tipo de alojamiento
    tipo = forms.CharField(required=False, label="Tipo de Alojamiento")
    
    # Campo de búsqueda por capacidad mínima
    capacidad = forms.IntegerField(required=False, label="Capacidad mínima")



class ReservaForm(forms.Form):
    codigo_reserva = forms.CharField(
        label="Código de Reserva",
        required=True,
        max_length=20,
        help_text="Máximo 20 caracteres"
    )
    
    fecha_salida = forms.DateTimeField(
        label="Fecha de Salida",
        initial=datetime.now,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    
    fecha_llegada = forms.DateTimeField(
        label="Fecha de Llegada",
        initial=datetime.now,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    
    numero_personas = forms.IntegerField(
        label="Número de Personas",
        min_value=1,
        required=True
    )
    
    precio = forms.DecimalField(
        label="Precio",
        max_digits=10,
        decimal_places=2,
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        super(ReservaForm, self).__init__(*args, **kwargs)
        
        usuariosDisponibles = helper.obtener_usuarios_select()
        self.fields["usuario"] = forms.ChoiceField(
            choices=usuariosDisponibles,
            widget=forms.Select,
            required=True
        )
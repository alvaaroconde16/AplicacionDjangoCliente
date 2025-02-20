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
    
    fecha_salida = forms.DateField(
        label="Fecha de Salida",
        initial=datetime.today().date(),
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    fecha_llegada = forms.DateField(
        label="Fecha de Llegada",
        initial=datetime.today().date(),
        widget=forms.DateInput(attrs={'type': 'date'})
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


class UsuarioForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre Completo",
        required=True,
        max_length=200,
        help_text="Ingrese el nombre completo"
    )
    
    correo = forms.EmailField(
        label="Correo Electrónico",
        required=True,
        help_text="Ingrese un correo electrónico válido"
    )
    
    telefono = forms.CharField(
        label="Teléfono",
        required=True,
        max_length=20,
        help_text="Ingrese un número de teléfono"
    )
    
    edad = forms.IntegerField(
        label="Edad",
        required=True,
        min_value=18,
        help_text="Debe ser mayor de 18 años"
    )
    
    contraseña = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        required=True,
        max_length=200,
        help_text="Ingrese una contraseña segura"
    )
    
    fecha_registro = forms.DateField(
        label="Fecha de Registro",
        initial=datetime.today().date(),
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    
    
class TransporteForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre del Transporte",
        required=True,
        max_length=200,
        help_text="Máximo 200 caracteres"
    )
    
    tipo = forms.CharField(
        label="Tipo de Transporte",
        required=True,
        max_length=50,
        help_text="Máximo 50 caracteres (Ej. Autobús, Avión, Tren)"
    )
    
    capacidad = forms.IntegerField(
        label="Capacidad",
        required=True,
        min_value=1,
        help_text="Número de personas que puede transportar"
    )
    
    precio_base = forms.DecimalField(
        label="Precio Base",
        required=True,
        max_digits=10,
        decimal_places=2,
        help_text="Precio base del transporte"
    )

    fecha_disponibilidad = forms.DateField(
        label="Fecha de Disponibilidad",
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Fecha en que el transporte estará disponible"
    )

    descripcion = forms.CharField(
        label="Descripción",
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Opcional: Descripción adicional del transporte"
    )

    # Obtener los destinos usando el helper
    def __init__(self, *args, **kwargs):
        super(TransporteForm, self).__init__(*args, **kwargs)
        
        # Llamamos al helper para obtener los destinos
        destinosDisponibles = helper.obtener_destinos_select()
        
        # Creamos el campo de selección de destino
        self.fields["destino"] = forms.ChoiceField(
            choices=destinosDisponibles,
            widget=forms.Select,
            required=True,
            label="Destino"
        )
    

#######################################################################################################################################################################


class ReservaActualizarCodigoForm(forms.Form):
    codigo_reserva = forms.CharField(
        label="Código de Reserva",
        required=True,
        max_length=20,
        help_text="Máximo 20 caracteres"
    )


class UsuarioActualizarNombreForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre Completo",
        required=True,
        max_length=200,
        help_text="Ingrese el nombre completo"
    )
from django import forms
from .models import Usuario, Destino, Reserva, Comentario, Alojamiento, Promocion
from datetime import date, datetime
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.forms import UserCreationForm

class UsuarioForm(forms.ModelForm):
    
    class Meta:
        model = Usuario
        fields = ['nombre', 'correo', 'telefono', 'edad', 'contraseña', 'fecha_registro', 'imagen']
        help_texts = {
            "nombre": ("200 caracteres como máximo"),
        }
        widgets = {
            "fecha_registro":forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }
        
    
    def clean(self):
        #Validamos con el modelo actual
        super().clean()
        
        #Obtenemos los campos 
        nombre = self.cleaned_data.get('nombre')
        correo = self.cleaned_data.get('correo')
        telefono = self.cleaned_data.get('telefono')
        edad = self.cleaned_data.get('edad')
        contraseña = self.cleaned_data.get('contraseña')
        fecha_registro = self.cleaned_data.get('fecha_registro')

        
        #Comprobamos que no exista un usuario con ese nombre
        destinoNombre = Usuario.objects.filter(nombre=nombre).first()
        if(not destinoNombre is None
           ):
             if(not self.instance is None and destinoNombre.id == self.instance.id):
                 pass
             else:
                self.add_error('nombre','Ya existe un usuario con ese nombre')
        
        
        #Comprobamos que el formato del correo es válido
        if "@" not in correo or "." not in correo:
            raise forms.ValidationError('correo', 'Por favor, introduce un correo válido.')
    
    
        #Comprobamos que el telefono solo contenga números
        if not telefono.isdigit():
            raise forms.ValidationError('telefono', 'El teléfono debe contener solo números.')


        # Comprobamos la edad (debe ser mayor a 18)
        if edad < 18:
            raise forms.ValidationError('edad','La edad mínima es 18 años.')
        
        
        #Comprobamos que la contraseña tenga al menos 8 caracteres
        if len(contraseña) < 8:
            self.add_error('contraseña','Al menos debes indicar 8 caracteres')
            
            
        #Comprobamos que la fecha de publicación sea mayor que hoy
        fechaHoy = date.today()
        if fechaHoy > fecha_registro :
            self.add_error('fecha_registro','La fecha de registro debe ser igual o mayor a Hoy')
            
            
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data
            
            


class DestinoForm(forms.ModelForm):
    
    class Meta:
        model = Destino
        fields = ['nombre', 'pais', 'descripcion', 'popularidad']
        help_texts = {
            "nombre": ("200 caracteres como máximo"),
            "descripcion": "La descripción no debe exceder los 500 caracteres",
            "popularidad": "Valor entre 0 y 5",
        }
        
    
    def clean(self):
        #Validamos con el modelo actual
        super().clean()
        
        #Obtenemos los campos 
        nombre = self.cleaned_data.get('nombre')
        pais = self.cleaned_data.get('pais')
        descripcion = self.cleaned_data.get('descripcion')
        popularidad = self.cleaned_data.get('popularidad')

        
        #Comprobamos que no exista un destino con ese nombre
        destinoNombre = Destino.objects.filter(nombre=nombre).first()
        if(not destinoNombre is None
           ):
             if(not self.instance is None and destinoNombre.id == self.instance.id):
                 pass
             else:
                self.add_error('nombre','Ya existe un destino con ese nombre')
                
                
        # Validación de país: Verificamos que el campo no esté vacío y sea un país válido
        if not pais:
            self.add_error('pais', 'El país no puede estar vacío.')
        
                
        # Validación de descripción: Verificamos que la descripción no esté vacía y no exceda los 500 caracteres
        if not descripcion:
            self.add_error('descripcion', 'La descripción no puede estar vacía.')
        elif len(descripcion) > 500:
            self.add_error('descripcion', 'La descripción no debe exceder los 500 caracteres.')
        
        
        # Validación de popularidad: Verificamos que esté entre 0 y 5
        if not (0 <= popularidad <= 5):
            self.add_error('popularidad', 'La popularidad debe estar entre 0 y 5.')
            
            
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data
            
    


class ReservaForm(forms.ModelForm):
    
    class Meta:
        model = Reserva
        fields = ['codigo_reserva', 'fecha_salida', 'fecha_llegada', 'numero_personas', 'precio', 'usuario']
        help_texts = {
            "codigo_reserva": ("200 caracteres como máximo"),
            "fecha_salida": ("La fecha de salida debe ser igual o mayor a hoy"),
            "numero_personas": ("El número de personas debe ser 1 como mínimo"),
            "precio": ("El precio debe ser un valor positivo"),
        }
        widgets = {
            "fecha_salida":forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "fecha_llegada":forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }   
        
    
    def clean(self):
        #Validamos con el modelo actual
        super().clean()
        
        #Obtenemos los campos 
        codigo_reserva = self.cleaned_data.get('codigo_reserva')
        fecha_salida = self.cleaned_data.get('fecha_salida')
        fecha_llegada = self.cleaned_data.get('fecha_llegada')
        numero_personas = self.cleaned_data.get('numero_personas')
        precio = self.cleaned_data.get('precio')
        usuario = self.cleaned_data.get('usuario')
        
        
        #Comprobamos que no exista una reserva con ese código
        codigoReserva = Reserva.objects.filter(codigo_reserva=codigo_reserva).first()
        if(not codigoReserva is None
           ):
             if(not self.instance is None and codigoReserva.id == self.instance.id):
                 pass
             else:
                self.add_error('codigo_reserva','Ya existe una reserva con ese código de reserva')
                
        
        fechaHoy = timezone.now()
        # Validación de fecha_salida: Verificamos que la fecha de salida no sea anterior a hoy
        if fecha_salida < fechaHoy:
            self.add_error('fecha_salida', 'La fecha de salida no puede ser anterior a hoy')
            
        
        # Validación de fecha_llegada: Verificamos que la fecha de llegada no sea anterior a la fecha de salida
        if fecha_llegada < fecha_salida:
            self.add_error('fecha_llegada', 'La fecha de llegada no puede ser anterior a la fecha de salida')
        
                
        # Validación de numero_personas: Verificamos que el número de personas sea al menos 1
        if numero_personas < 1:
            self.add_error('numero_personas', 'El número de personas debe ser al menos 1')


        # Validación de precio: Verificamos que el precio sea mayor que 0
        if precio <= 0:
            self.add_error('precio', 'El precio debe ser un valor positivo')
            
            
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data
    
    


class AlojamientoForm(forms.ModelForm):
    
    class Meta:
        model = Alojamiento
        fields = ['nombre', 'direccion', 'capacidad', 'tipo', 'destino', 'reserva']
        help_texts = {
            "nombre": ("200 caracteres como máximo"),
            "capacidad": "Capacidad de 1 como mínimo",
        }
        widgets = {
            'reserva': forms.CheckboxSelectMultiple(),  # Esto permitirá la selección múltiple de reservas
        }
        
    
    def clean(self):
        #Validamos con el modelo actual
        super().clean()
        
        #Obtenemos los campos 
        nombre = self.cleaned_data.get('nombre')
        direccion = self.cleaned_data.get('direccion')
        capacidad = self.cleaned_data.get('capacidad')
        tipo = self.cleaned_data.get('tipo')
        destino = self.cleaned_data.get('destino')
        reserva = self.cleaned_data.get('reserva')

        
        #Comprobamos que no exista un alojamiento con ese nombre
        alojamientoNombre = Alojamiento.objects.filter(nombre=nombre).first()
        if(not alojamientoNombre is None
           ):
             if(not self.instance is None and alojamientoNombre.id == self.instance.id):
                 pass
             else:
                self.add_error('nombre','Ya existe un alojamiento con ese nombre')
                
                
        # Validación: Comprobamos que la descripción no exceda los 500 caracteres
        if len(direccion) > 500:
            self.add_error('direccion', 'La dirección no puede exceder los 500 caracteres.')
                

        # Validación: Comprobamos que la capacidad sea al menos 1
        if capacidad < 1:
            self.add_error('capacidad', 'La capacidad debe de ser de al menos 1 persona.')
            
            
         # Validación: Comprobamos que se haya seleccionado un destino
        if not destino:
            self.add_error('destino', 'Debe seleccionar un destino para el alojamiento.')


        # Validación: Comprobamos que se haya seleccionado al menos una reserva
        if not reserva:
            self.add_error('reserva', 'Debe seleccionar al menos una reserva para este alojamiento.')
            
            
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data
    


class ComentarioForm(forms.ModelForm):
    
    class Meta:
        model = Comentario
        fields = ['titulo', 'contenido', 'calificacion', 'usuario']
        help_texts = {
            "nombre": ("200 caracteres como máximo"),
            "contenido": ("No puede exceder los 500 caracteres"),
        }
        widgets = {
            "fecha_comentario":forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }
        
    
    def clean(self):
        #Validamos con el modelo actual
        super().clean()
        
        #Obtenemos los campos 
        titulo = self.cleaned_data.get('titulo')
        contenido = self.cleaned_data.get('contenido')
        calificacion = self.cleaned_data.get('calificacion')
        usuario = self.cleaned_data.get('usuario')

        
        #Comprobamos que no exista un alojamiento con ese nombre
        comentarioNombre = Comentario.objects.filter(titulo=titulo).first()
        if(not comentarioNombre is None
           ):
             if(not self.instance is None and comentarioNombre.id == self.instance.id):
                 pass
             else:
                self.add_error('titulo','Ya existe un comentario con ese título')
                
                
        # Validación: Comprobamos que la descripción no exceda los 500 caracteres
        if len(contenido) > 500:
            self.add_error('contenido', 'El contenido no puede exceder los 500 caracteres.')
            
        # Validación: Comprobamos que se haya seleccionado un destino
        if not (0 <= calificacion <= 5):
            self.add_error('calificacion', 'La calificacion debe estar entre 0 y 5.')
            
            
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data
    


class PromocionForm(forms.ModelForm):
    
    class Meta:
        model = Promocion
        fields = ['nombre', 'descripcion', 'descuento_porcentaje', 'fecha_inicio', 'fecha_fin', 'activo', 'alojamiento', 'destino']
        help_texts = {
            "nombre": ("100 caracteres como máximo"),
            "descripcion": ("Descripción detallada de la promoción."),
            "descuento_porcentaje": ("Ingrese un porcentaje entre 0 y 100."),
        }
        widgets = {
            "fecha_inicio": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "fecha_fin": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }
    
    def clean(self):
        # Validamos los datos con el modelo actual
        super().clean()

        # Obtenemos los campos
        nombre = self.cleaned_data.get('nombre')
        descuento_porcentaje = self.cleaned_data.get('descuento_porcentaje')
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        fecha_fin = self.cleaned_data.get('fecha_fin')

        # Validación: Verificar que no exista una promoción con el mismo nombre
        promo_existente = Promocion.objects.filter(nombre=nombre).first()
        if promo_existente and (not self.instance or promo_existente.id != self.instance.id):
            self.add_error('nombre', 'Ya existe una promoción con este nombre.')

        # Validación: El descuento debe estar entre 0 y 100
        if not (0 <= descuento_porcentaje <= 100):
            self.add_error('descuento_porcentaje', 'El porcentaje de descuento debe estar entre 0 y 100.')

        # Validación: La fecha de inicio debe ser anterior a la fecha de fin
        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            self.add_error('fecha_fin', 'La fecha de fin debe ser posterior a la fecha de inicio.')

        # Validación: La fecha de inicio no puede ser en el pasado
        if fecha_inicio and fecha_inicio < date.today():
            self.add_error('fecha_inicio', 'La fecha de inicio no puede ser en el pasado.')

        # Siempre devolvemos el conjunto de datos
        return self.cleaned_data
    
    
    
########################################################################################################################################################################

class BusquedaUsuarioForm(forms.Form):
    # Campo de búsqueda por nombre
    nombre = forms.CharField(required=False, label="Nombre")

    # Campo de búsqueda por correo
    correo = forms.EmailField(required=False, label="Correo Electrónico")

    # Campo para edad
    edad = forms.IntegerField(required=False, label="Edad")

    def clean(self):
        # Llamamos al método clean de la clase base para validar el formulario
        cleaned_data = super().clean()

        # Obtenemos los valores de los campos
        nombre = cleaned_data.get('nombre')
        correo = cleaned_data.get('correo')
        edad = cleaned_data.get('edad')


        # Verificamos que al menos un campo tenga un valor
        if (not nombre 
            and not correo 
            and edad is None ):
            
            self.add_error('nombre', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('correo', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('edad', 'Debe introducir al menos un valor en un campo del formulario')


        else:
            # Si el nombre se ha introducido, debe tener al menos 3 caracteres
            if nombre and len(nombre) < 3:
                self.add_error('nombre', 'El nombre debe tener al menos 3 caracteres')

            # Si la edad se ha introducido y es menor o igual a 0
            if edad is not None and edad <= 0:
                self.add_error('edad', 'La edad no puede ser menor que 0')

        return cleaned_data
    


class BusquedaReservaForm(forms.Form):
    # Campo de búsqueda por nombre de reserva
    codigo_reserva = forms.CharField(required=False, label="Código de la Reserva")

    # Campo de búsqueda por fecha de reserva
    fecha = forms.DateField(required=False, label="Fecha de la Reserva", widget=forms.DateInput(attrs={'type': 'date'}))

    # Campo de búsqueda por estado de la reserva
    numero_personas = forms.IntegerField(required=False, label="Número de personas")

    def clean(self):
        cleaned_data = super().clean()
        
        # Obtener los valores del formulario
        codigo_reserva = cleaned_data.get('codigo_reserva')
        fecha = cleaned_data.get('fecha')
        numero_personas = cleaned_data.get('numero_personas')


        # Verificamos que al menos un campo tenga un valor
        if (not codigo_reserva 
            and not fecha 
            and not numero_personas):
            self.add_error(None, 'Debe introducir al menos un valor en un campo del formulario')
        
        else:
            # Si el nombre se ha introducido, debe tener al menos 3 caracteres
            if codigo_reserva and len(codigo_reserva) < 3:
                self.add_error('nombre', 'El nombre debe tener al menos 3 caracteres')


            fechaHoy = date.today()
            # Validación de fecha: Verificamos que la fecha no sea anterior a hoy
            if fecha and fecha < fechaHoy:  # Asegúrate de que 'fecha' no sea None
                self.add_error('fecha', 'La fecha no puede ser anterior a hoy')


            # Si se ha introducido un estado, debe ser uno de los valores válidos
            if numero_personas and numero_personas <= 0:
                self.add_error('numero_personas', 'El numero de personas debe ser mayor que 0')

        return cleaned_data



class BusquedaDestinoForm(forms.Form):
    # Campo de búsqueda por nombre del destino
    nombre = forms.CharField(required=False, label="Nombre del Destino")

    # Campo de búsqueda por país del destino
    pais = forms.CharField(required=False, label="País")

    # Campo de búsqueda por popularidad
    popularidad = forms.FloatField(
        required=False, 
        label="Popularidad", 
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    def clean(self):
        cleaned_data = super().clean()
        
        # Obtener los valores del formulario
        nombre = cleaned_data.get('nombre')
        pais = cleaned_data.get('pais')
        popularidad = cleaned_data.get('popularidad')

        # Verificamos que al menos un campo tenga un valor
        if not nombre and not pais and popularidad is None:
            self.add_error(None, 'Debe introducir al menos un valor en un campo del formulario')
        else:
            # Validación del nombre
            if nombre and len(nombre) < 3:
                self.add_error('nombre', 'El nombre debe tener al menos 3 caracteres')
            
            # Validación de popularidad mínima
            if popularidad is not None and (popularidad < 0 or popularidad > 5):
                self.add_error('popularidad', 'La popularidad debe estar entre 0 y 5')

        return cleaned_data
        
 

class BusquedaAlojamientoForm(forms.Form):
    # Campo de búsqueda por nombre de alojamiento
    nombre = forms.CharField(required=False, label="Nombre del Alojamiento")
    
    # Campo de búsqueda por tipo de alojamiento
    tipo = forms.CharField(required=False, label="Tipo de Alojamiento")
    
    # Campo de búsqueda por capacidad mínima
    capacidad = forms.IntegerField(required=False, label="Capacidad")

    def clean(self):
        cleaned_data = super().clean()
        
        nombre = cleaned_data.get('nombre')
        tipo = cleaned_data.get('tipo')
        capacidad = cleaned_data.get('capacidad')

        # Verificamos que al menos un campo tenga un valor
        if not nombre and not tipo and not capacidad:
            self.add_error(None, 'Debe introducir al menos un valor en un campo del formulario.')
        
        return cleaned_data
    


class BusquedaComentarioForm(forms.Form):
    # Campo de búsqueda por nombre del destino
    titulo = forms.CharField(required=False, label="Título del Comentario")

    # Campo de búsqueda por país del destino
    contenido = forms.CharField(required=False, label="Contenido")

    # Campo de búsqueda por popularidad
    calificacion = forms.FloatField(
        required=False, 
        label="Calificacion", 
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    def clean(self):
        cleaned_data = super().clean()
        
        # Obtener los valores del formulario
        titulo = cleaned_data.get('titulo')
        contenido = cleaned_data.get('contenido')
        calificacion = cleaned_data.get('calificacion')

        # Verificamos que al menos un campo tenga un valor
        if not titulo and not contenido and calificacion is None:
            self.add_error(None, 'Debe introducir al menos un valor en un campo del formulario')
        else:
            # Validación del nombre
            if titulo and len(titulo) < 3:
                self.add_error('titulo', 'El titulo debe tener al menos 3 caracteres')
            
            # Validación de calificacion mínima
            if calificacion is not None and (calificacion < 0 or calificacion > 5):
                self.add_error('calificacion', 'La calificacion debe estar entre 0 y 5')

        return cleaned_data
    


class BusquedaPromocionForm(forms.Form):
    # Campo de búsqueda por nombre de la promoción
    nombre = forms.CharField(required=False, label="Nombre de la Promoción")

    # Campo de búsqueda por descripción
    descripcion = forms.CharField(required=False, label="Descripción")

    # Campo de búsqueda por descuento
    descuento_porcentaje = forms.FloatField(
        required=False, 
        label="Descuento (%)", 
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def clean(self):
        cleaned_data = super().clean()
        
        # Obtener los valores del formulario
        nombre = cleaned_data.get('nombre')
        descripcion = cleaned_data.get('descripcion')
        descuento_porcentaje = cleaned_data.get('descuento_porcentaje')

        # Verificamos que al menos un campo tenga un valor
        if not nombre and not descripcion and descuento_porcentaje is None:
            self.add_error(None, 'Debe introducir al menos un valor en un campo del formulario')
        else:
            # Validación del nombre
            if nombre and len(nombre) < 3:
                self.add_error('nombre', 'El nombre debe tener al menos 3 caracteres')
            
            # Validación del porcentaje de descuento
            if descuento_porcentaje is not None and (descuento_porcentaje < 0 or descuento_porcentaje > 100):
                self.add_error('descuento_porcentaje', 'El descuento debe estar entre 0 y 100')

        return cleaned_data
    

########################################################################################################################################################################


class RegistroForm(UserCreationForm):
    roles = (
        ("", "NINGUNO"),
        (Usuario.CLIENTE, 'cliente'),
        (Usuario.PROVEEDOR, 'proveedor'),
    )

    rol = forms.ChoiceField(choices=roles)
    empresa = forms.CharField(max_length=200, required=False, label="Nombre de la Empresa")
    rating = forms.FloatField(required=False,label="Calificación Promedia")

    class Meta:
        model = Usuario
        fields = ('nombre', 'username', 'email', 'telefono', 'password1', 'password2', 'rol')


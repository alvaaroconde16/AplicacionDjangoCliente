from django.shortcuts import render,redirect, get_object_or_404
from .models import Usuario, Destino, Reserva, Comentario, Alojamiento, Cliente, Proveedor
from django.db.models import Q, Sum
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
def index(request):
    
    if(not "fecha_inicio" in request.session):
        request.session["fecha_inicio"] = datetime.now().strftime('%d/%m/%Y %H:%M')
    
    return render(request, 'principal.html')


@permission_required('viajes.listar_usuarios')
#Empezamos mostrando una lista con todos los usuarios
def listar_usuarios(request):
    usuario = Usuario.objects.select_related('pasaporte').all()

    return render (request, 'usuarios/lista.html', {'usuarios_mostrar':usuario})


#Empezamos mostrando una lista con todas las reservas
def listar_reservas(request):
    reserva = Reserva.objects.select_related('usuario').all()

    return render (request, 'reservas/reservas.html', {'reservas_mostrar':reserva})


#Ahora vamos a mostrar todas las reservas que tiene cada usuario. Usamos un parámetro entero como es el id_usuario
def listar_reservasUsuario(request, id_usuario):
    reserva = Reserva.objects.select_related("usuario").filter(usuario_id=id_usuario)

    return render(request, 'reservas/reserva_usuario.html', {'reservas_mostrar':reserva})


#Mostramos las reservas que estén comprendidas entre un año de inicio y un año de fin. Usamos un parámetro str como es la fecha_inicio y fecha_fin y AND
def reservas_rango(request, fecha_inicio, fecha_fin):
    reserva = Reserva.objects.select_related("usuario").filter(fecha_salida__gte=fecha_inicio, fecha_llegada__lte=fecha_fin)

    return render(request, 'reservas/reservas.html', {'reservas_mostrar':reserva})


#Vamos a mostrar las reservas que no tienen ningún extra asociado. Usamos la tabla intermedia ExtraReserva y usamos el None.
def reservas_sin_extras(request):
    reserva = Reserva.objects.select_related("usuario").filter(extrareserva=None)

    return render(request, 'reservas/reservas.html', {'reservas_mostrar': reserva})


#Mostramos todos los destinos
def listar_destinos(request):
    destino = Destino.objects.all()

    return render(request, 'destinos/destinos.html', {'destinos_mostrar':destino})


#Mostramos todos los destinos
def listar_alojamientos(request):
    alojamiento = Alojamiento.objects.all()

    return render(request, 'destinos/alojamientos.html', {'alojamientos_mostrar':alojamiento})


def listar_comentarios(request):
    comentario = Comentario.objects.select_related('usuario').all()

    return render(request, 'usuarios/comentarios.html', {'comentarios_mostrar':comentario})


def listar_promociones(request):
    promocion = Promocion.objects.select_related('alojamiento').prefetch_related('destino').all()

    return render(request, 'promociones/lista.html', {'promociones_mostrar':promocion})



#vamos a mostrar todos los alojamientos asociados a un destino
def alojamientos_destino(request, id_destino):
    alojamiento = Alojamiento.objects.select_related("destino").filter(destino_id=id_destino)

    return render(request, 'destinos/alojamientos.html', {'alojamientos_mostrar':alojamiento})


@permission_required('viajes.pasaporte')
#Mostramos los usuarios que tengan en su pasaporte la misma nacionalidad o Española. Usamos el parámetro OR
def pasaporte_nacionalidad(request, nacionalidad):
    usuario = Usuario.objects.select_related("pasaporte").filter(Q(pasaporte__nacionalidad=nacionalidad) | Q(pasaporte__nacionalidad='Española'))

    return render(request, 'usuarios/lista.html', {'usuario':usuario})


# Vamos a mostrar el último usuario que comento. Usamos el order_by para ordenar la fecha de comentario y el limit para coger uno solo que será el último
def ultimo_usuario_comentar(request):
    comentario = Comentario.objects.select_related('usuario').order_by("-fecha_comentario")[:1].all()

    return render(request, 'usuarios/ultimoCom.html', {'comentarios_mostrar':comentario})



#Mostramos todos los comentarios de un usuario en específico
def comentarios_usuario(request, id_usuario):
    comentarios = Comentario.objects.select_related('usuario').filter(usuario_id=id_usuario).all()
    
    return render(request, 'usuarios/comentarios.html', {'comentarios_mostrar':comentarios})



#Mostramos la suma de todos los precios de las reservas. Usamos el parámetro aggregate el cual se usa para realizar cálculos en los datos de una tabla y 
#devolver un solo valor, en lugar de una lista de resultados. Podemos usar el Sum, el Avg, y el Count por ejemplo
def total_precios_reservas(request):
    total_precio = Reserva.objects.select_related("usuario").aggregate(Sum('precio'))  

    return render(request, 'reservas/total_precios.html', {'precio_mostrar':total_precio})


########################################################################################################################################################################

################################################################        AQUÍ COMIENZAN LOS CREATE      #################################################################

@permission_required('viajes.crear_usuario')
#A partir de aquí, creamos todos los formulario de creación.
def usuario_create(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES) # Nos aseguramos de incluir request.FILES
        if form.is_valid():
            form.save()  # Guarda el nuevo usuario en la base de datos
            messages.success(request, 'Usuario creado con éxito.')
            return redirect('listar_usuarios')  # Redirige a la lista de usuarios después de crear
    else:
        form = UsuarioForm()  # Si la solicitud es GET, muestra el formulario vacío

    return render(request, 'formularios/usuario_form.html', {'form': form})


@permission_required('viajes.crear_destino')
def destino_create(request):
    if request.method == 'POST':
        form = DestinoForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo destino en la base de datos
            messages.success(request, 'Destino creado con éxito.')
            return redirect('listar_destinos')  # Redirige a la lista de destinos después de crear
    else:
        form = DestinoForm()  # Si la solicitud es GET, muestra el formulario vacío

    return render(request, 'formularios/destino_form.html', {'form': form})


@login_required
def reserva_create(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)  # Guarda la nueva reserva en la base de datos
            
            if request.user.rol != 1:
                reserva.usuario = request.user

            reserva.save()
            messages.success(request, 'Reserva creada con éxito.')
            if request.user.rol == 1:
                return redirect('listar_reservas')
            else:
                return redirect('listar_reservasUsuario', id_usuario=request.user.id)
    else:
        # Si el usuario es administrador, le permitimos seleccionar otro usuario
        if request.user.rol == 1:
            form = ReservaForm()  # Mostrar formulario normal
        else:
            # Si el usuario no es administrador, pre-poblar el campo con su nombre y hacerlo solo de lectura
            form = ReservaForm()
            form.fields['usuario'].initial = request.user  # Pre-poblar con el nombre del usuario
            form.fields['usuario'].widget = forms.HiddenInput()  # Ocultamos el campo

    return render(request, 'formularios/reserva_form.html', {'form': form})


@login_required
def alojamiento_create(request):
    if request.method == 'POST':
        form = AlojamientoForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda la nueva reserva en la base de datos
            messages.success(request, 'Alojamiento creado con éxito.')
            return redirect('listar_alojamientos')  # Redirige a la lista de reservas después de crear
    else:
        form = AlojamientoForm()  # Si la solicitud es GET, muestra el formulario vacío

    return render(request, 'formularios/alojamiento_form.html', {'form': form})


@login_required
def comentario_create(request):
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)  # Guarda la nueva reserva en la base de datos
            
            if request.user.rol != 1:
                comentario.usuario = request.user
            
            comentario.save()
            messages.success(request, 'Comentario creado con éxito.')
            if request.user.rol == 1:
                return redirect('listar_comentarios')
            else:
                return redirect('comentarios_usuario', id_usuario=request.user.id)
    else:
        # Si el usuario es administrador, le permitimos seleccionar otro usuario
        if request.user.rol == 1:
            form = ComentarioForm()  # Mostrar formulario normal
        else:
            # Si el usuario no es administrador, pre-poblar el campo con su nombre y hacerlo solo de lectura
            form = ComentarioForm()
            form.fields['usuario'].initial = request.user  # Pre-poblar con el nombre del usuario
            form.fields['usuario'].widget = forms.HiddenInput()  # Ocultamos el campo

    return render(request, 'formularios/comentario_form.html', {'form': form})



@permission_required('viajes.crear_promocion')
def promocion_create(request):
    if request.method == 'POST':
        form = PromocionForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda la nueva promoción en la base de datos
            messages.success(request, 'Promoción creada con éxito.')
            return redirect('listar_promociones')  # Redirige a la lista de promociones después de crear
    else:
        form = PromocionForm()  # Si la solicitud es GET, muestra el formulario vacío

    return render(request, 'formularios/promocion_form.html', {'form': form})



########################################################################################################################################################################

#################################################################        AQUÍ COMIENZAN LOS READ      ##################################################################

@permission_required('viajes.buscar_usuario')
def usuario_busqueda(request):
    # Si se ha enviado el formulario (request.GET contiene datos)
    if request.GET:
        formulario = BusquedaUsuarioForm(request.GET)

        if formulario.is_valid():
            mensaje_busqueda = "Se ha buscado por los siguientes filtros:\n"
            usuarios = Usuario.objects.all()  # Empezamos con todos los usuarios

            # Obtenemos los valores de los campos filtrados
            nombre = formulario.cleaned_data.get('nombre')
            correo = formulario.cleaned_data.get('correo')
            edad = formulario.cleaned_data.get('edad')


            # Filtro por nombre
            if nombre:
                usuarios = usuarios.filter(nombre__icontains=nombre)
                mensaje_busqueda += f"Nombre que contenga: {nombre}\n"

            # Filtro por correo
            if correo:
                usuarios = usuarios.filter(correo__icontains=correo)
                mensaje_busqueda += f"Correo que contenga: {correo}\n"

            # Filtro por edad
            if edad is not None:
                usuarios = usuarios.filter(edad__gte=edad)
                mensaje_busqueda += f"Edad mínima: {edad}\n"


            # Pasamos los usuarios filtrados y el mensaje a la plantilla
            return render(request, 'usuarios/lista.html', {
                'usuarios_mostrar': usuarios,
                'mensaje_busqueda': mensaje_busqueda
            })
    else:
        formulario = BusquedaUsuarioForm()

    return render(request, 'formularios/usuario_busqueda.html', {'formulario': formulario})



@login_required
def reserva_busqueda(request):
    # Si se ha enviado el formulario (request.GET contiene datos)
    if request.GET:
        formulario = BusquedaReservaForm(request.GET)

        if formulario.is_valid():
            # Obtenemos los valores de los campos filtrados
            codigo_reserva = formulario.cleaned_data.get('codigo_reserva')
            fecha = formulario.cleaned_data.get('fecha')
            numero_personas = formulario.cleaned_data.get('numero_personas')

            # Empezamos con todos las reservas
            if request.user.rol == 1:
                reservas = Reserva.objects.all()
            else :
                reservas = Reserva.objects.filter(usuario = request.user)

            # Filtro por nombre de reserva
            if codigo_reserva:
                reservas = reservas.filter(codigo_reserva__icontains=codigo_reserva)

            # Filtro por fecha de reserva
            if fecha:
                reservas = reservas.filter(fecha_salida__date=fecha)

            # Filtro por estado de la reserva
            if numero_personas:
                reservas = reservas.filter(numero_personas=numero_personas)


            # Mensaje con los filtros aplicados
            mensaje_busqueda = "Se han encontrado las siguientes reservas con los filtros aplicados:\n"

            if codigo_reserva:
                mensaje_busqueda += f"Nombre que contenga: {codigo_reserva}\n"

            if fecha:
                mensaje_busqueda += f"Fecha exacta: {fecha}\n"

            if numero_personas:
                mensaje_busqueda += f"Numero de personas: {numero_personas}\n"

            # Pasamos las reservas filtradas y el mensaje a la plantilla
            return render(request, 'reservas/reservas.html', {
                'reservas_mostrar': reservas,
                'mensaje_busqueda': mensaje_busqueda
            })
    else:
        formulario = BusquedaReservaForm()

    return render(request, 'formularios/reserva_busqueda.html', {'formulario': formulario})


def destino_busqueda(request):
    if request.GET:

        formulario = BusquedaDestinoForm(request.GET)

        if formulario.is_valid():

            # Obtenemos los valores filtrados
            nombre = formulario.cleaned_data.get('nombre')
            pais = formulario.cleaned_data.get('pais')
            popularidad_minima = formulario.cleaned_data.get('popularidad_minima')

            # Filtrar destinos
            destinos = Destino.objects.all()

            if nombre:
                destinos = destinos.filter(nombre__icontains=nombre)

            if pais:
                destinos = destinos.filter(pais__icontains=pais)

            if popularidad_minima is not None:
                destinos = destinos.filter(popularidad__gte=popularidad_minima)


            mensaje_busqueda = "Resultados de búsqueda:"
            if nombre:
                mensaje_busqueda += f" Nombre que contiene: {nombre}."

            if pais:
                mensaje_busqueda += f" País que contiene: {pais}."

            if popularidad_minima is not None:
                mensaje_busqueda += f" Popularidad mínima: {popularidad_minima}."

            return render(request, 'destinos/destinos.html', {
                'destinos_mostrar': destinos,
                'mensaje_busqueda': mensaje_busqueda
            })
    else:
        formulario = BusquedaDestinoForm()

    return render(request, 'formularios/destino_busqueda.html', {'formulario': formulario})



def alojamiento_busqueda(request):
    # Si se envía el formulario con datos
    if request.GET:
        formulario = BusquedaAlojamientoForm(request.GET)
        
        if formulario.is_valid():
            # Obtener datos filtrados
            nombre = formulario.cleaned_data.get('nombre')
            tipo = formulario.cleaned_data.get('tipo')
            capacidad = formulario.cleaned_data.get('capacidad')

            # Filtrar los alojamientos
            alojamientos = Alojamiento.objects.all()
            if nombre:
                alojamientos = alojamientos.filter(nombre__icontains=nombre)
            if tipo:
                alojamientos = alojamientos.filter(tipo__icontains=tipo)
            if capacidad:
                alojamientos = alojamientos.filter(capacidad__gte=capacidad)
            
            return render(request, 'destinos/alojamientos.html', {
                'alojamientos_mostrar': alojamientos,
                'mensaje_busqueda': 'Se encontraron resultados para su búsqueda.',
            })
    else:
        formulario = BusquedaAlojamientoForm()

    return render(request, 'formularios/alojamiento_busqueda.html', {'formulario': formulario})



def comentario_busqueda(request):
    # Si se envía el formulario con datos
    if request.GET:

        formulario = BusquedaComentarioForm(request.GET)
        
        if formulario.is_valid():
            # Obtener datos filtrados
            titulo = formulario.cleaned_data.get('titulo')
            contenido = formulario.cleaned_data.get('contenido')
            calificacion = formulario.cleaned_data.get('calificacion')

            # Filtrar los alojamientos
            comentarios = Comentario.objects.all()
            
            if titulo:
                comentarios = comentarios.filter(titulo__icontains=titulo)

            if contenido:
                comentarios = comentarios.filter(contenido__icontains=comentarios)

            if calificacion is not None:
                comentarios = comentarios.filter(calificacion__gte=calificacion)


            mensaje_busqueda = "Resultados de búsqueda:"
            if titulo:
                mensaje_busqueda += f" Titulo que contiene: {titulo}."

            if contenido:
                mensaje_busqueda += f" Contenido que contiene: {contenido}."

            if calificacion is not None:
                mensaje_busqueda += f" Calificación: {calificacion}."


            return render(request, 'usuarios/comentarios.html', {
                'comentarios_mostrar': comentarios,
                'mensaje_busqueda': 'Se encontraron resultados para su búsqueda.',
            })
    else:
        formulario = BusquedaComentarioForm()

    return render(request, 'formularios/comentario_busqueda.html', {'formulario': formulario})



def promocion_busqueda(request):
    if request.GET:
        formulario = BusquedaPromocionForm(request.GET)

        if formulario.is_valid():
            # Obtenemos los valores filtrados
            nombre = formulario.cleaned_data.get('nombre')
            descripcion = formulario.cleaned_data.get('descripcion')
            descuento_porcentaje = formulario.cleaned_data.get('descuento_porcentaje')

            # Filtrar promociones
            promociones = Promocion.objects.all()

            if nombre:
                promociones = promociones.filter(nombre__icontains=nombre)

            if descripcion:
                promociones = promociones.filter(descripcion__icontains=descripcion)

            if descuento_porcentaje is not None:
                promociones = promociones.filter(descuento_porcentaje__gte=descuento_porcentaje)

            # Construir mensaje de búsqueda
            mensaje_busqueda = "Resultados de búsqueda:"
            if nombre:
                mensaje_busqueda += f" Nombre que contiene: {nombre}."

            if descripcion:
                mensaje_busqueda += f" Descripción que contiene: {descripcion}."

            if descuento_porcentaje is not None:
                mensaje_busqueda += f" Descuento mínimo: {descuento_porcentaje}%."

            return render(request, 'promociones/lista.html', {
                'promociones_mostrar': promociones,
                'mensaje_busqueda': mensaje_busqueda
            })
    else:
        formulario = BusquedaPromocionForm()

    return render(request, 'formularios/promocion_busqueda.html', {'formulario': formulario})


########################################################################################################################################################################

################################################################        AQUÍ COMIENZAN LOS UPDATE      #################################################################

@permission_required('viajes.actualizar_usuario')
def actualizar_usuario(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)

    # Variable para almacenar los datos del formulario
    datosFormulario = None
    archivosFormulario = None
    
    # Si la solicitud es POST, obtenemos los datos del formulario
    if request.method == "POST":
        datosFormulario = request.POST
        archivosFormulario = request.FILES

    # Creamos el formulario con los datos, y si es un POST, llenamos con los datos del usuario
    form = UsuarioForm(datosFormulario, archivosFormulario, instance = usuario)


    # Si el método es POST y el formulario es válido
    if (request.method == "POST"): 
        if form.is_valid():
            try:
                # Guardamos los cambios del formulario
                form.save()
                
                # Mostramos un mensaje de éxito
                messages.success(request, f"Se ha actualizado el usuario {form.cleaned_data.get('nombre')} correctamente")
                
                # Redirigimos al usuario a la lista de usuarios
                return redirect('listar_usuarios')
            
            except Exception as error:
                print(error)  # En un entorno real, deberíamos loguear esto o mostrarlo en la interfaz
        else:
            print("Errores del formulario:", form.errors)

    # Renderizamos el formulario en caso de GET o si el formulario no es válido
    return render(request, 'formularios/actualizar_usuario.html', {'form': form, 'usuario': usuario})



@permission_required('viajes.actualizar_reserva')
def actualizar_reserva(request, reserva_id):
    reserva = Reserva.objects.get(id=reserva_id)

    # Variable para almacenar los datos del formulario
    datosFormulario = None
    
    # Si la solicitud es POST, obtenemos los datos del formulario
    if request.method == "POST":
        datosFormulario = request.POST

    # Creamos el formulario con los datos, y si es un POST, llenamos con los datos del usuario
    form = ReservaForm(datosFormulario, instance = reserva)


    # Si el método es POST y el formulario es válido
    if (request.method == "POST"): 
        if form.is_valid():
            try:
                # Guardamos los cambios del formulario
                form.save()
                
                # Mostramos un mensaje de éxito
                messages.success(request, f"Se ha actualizado la reserva {form.cleaned_data.get('codigo_reserva')} correctamente")
                
                # Redirigimos al usuario a la lista de usuarios
                return redirect('listar_reservas')
            
            except Exception as error:
                print(error)  # En un entorno real, deberíamos loguear esto o mostrarlo en la interfaz
        else:
            print("Errores del formulario:", form.errors)

    # Renderizamos el formulario en caso de GET o si el formulario no es válido
    return render(request, 'formularios/actualizar_reserva.html', {'form': form, 'usuario': reserva})



@permission_required('viajes.actualizar_destino')
def actualizar_destino(request, destino_id):
    destino = Destino.objects.get(id=destino_id)

    # Variable para almacenar los datos del formulario
    datosFormulario = None
    
    # Si la solicitud es POST, obtenemos los datos del formulario
    if request.method == "POST":
        datosFormulario = request.POST

    # Creamos el formulario con los datos, y si es un POST, llenamos con los datos del usuario
    form = DestinoForm(datosFormulario, instance = destino)


    # Si el método es POST y el formulario es válido
    if (request.method == "POST"): 
        if form.is_valid():
            try:
                # Guardamos los cambios del formulario
                form.save()
                
                # Mostramos un mensaje de éxito
                messages.success(request, f"Se ha actualizado el destino {form.cleaned_data.get('nombre')} correctamente")
                
                # Redirigimos al usuario a la lista de usuarios
                return redirect('listar_destinos')
            
            except Exception as error:
                print(error)  # En un entorno real, deberíamos loguear esto o mostrarlo en la interfaz
        else:
            print("Errores del formulario:", form.errors)

    # Renderizamos el formulario en caso de GET o si el formulario no es válido
    return render(request, 'formularios/actualizar_destino.html', {'form': form, 'destino': destino}) 



@permission_required('viajes.actualizar_alojamiento')
def actualizar_alojamiento(request, alojamiento_id):
    alojamiento = Alojamiento.objects.get(id=alojamiento_id)

    # Variable para almacenar los datos del formulario
    datosFormulario = None
    
    # Si la solicitud es POST, obtenemos los datos del formulario
    if request.method == "POST":
        datosFormulario = request.POST

    # Creamos el formulario con los datos, y si es un POST, llenamos con los datos del usuario
    form = AlojamientoForm(datosFormulario, instance = alojamiento)


    # Si el método es POST y el formulario es válido
    if (request.method == "POST"): 
        if form.is_valid():
            try:
                # Guardamos los cambios del formulario
                form.save()
                
                # Mostramos un mensaje de éxito
                messages.success(request, f"Se ha actualizado el alojamiento {form.cleaned_data.get('nombre')} correctamente")
                
                # Redirigimos al usuario a la lista de usuarios
                return redirect('listar_alojamientos')
            
            except Exception as error:
                print(error)  # En un entorno real, deberíamos loguear esto o mostrarlo en la interfaz
        else:
            print("Errores del formulario:", form.errors)

    # Renderizamos el formulario en caso de GET o si el formulario no es válido
    return render(request, 'formularios/actualizar_alojamiento.html', {'form': form, 'alojamiento': alojamiento}) 


@permission_required('viajes.actualizar_comentario')
def actualizar_comentario(request, comentario_id):
    comentario = Comentario.objects.get(id=comentario_id)

    # Variable para almacenar los datos del formulario
    datosFormulario = None
    
    # Si la solicitud es POST, obtenemos los datos del formulario
    if request.method == "POST":
        datosFormulario = request.POST

    # Creamos el formulario con los datos, y si es un POST, llenamos con los datos del usuario
    form = ComentarioForm(datosFormulario, instance = comentario)


    # Si el método es POST y el formulario es válido
    if (request.method == "POST"): 
        if form.is_valid():
            try:
                # Guardamos los cambios del formulario
                form.save()
                
                # Mostramos un mensaje de éxito
                messages.success(request, f"Se ha actualizado el comentario {form.cleaned_data.get('titulo')} correctamente")
                
                # Redirigimos al usuario a la lista de usuarios
                return redirect('listar_comentarios')
            
            except Exception as error:
                print(error)  # En un entorno real, deberíamos loguear esto o mostrarlo en la interfaz
        else:
            print("Errores del formulario:", form.errors)

    # Renderizamos el formulario en caso de GET o si el formulario no es válido
    return render(request, 'formularios/actualizar_comentario.html', {'form': form, 'comentario': comentario})



@permission_required('viajes.actualizar_promocion')
def actualizar_promocion(request, promocion_id):
    promocion = Promocion.objects.get(id=promocion_id)

    # Variable para almacenar los datos del formulario
    datosFormulario = None
    
    # Si la solicitud es POST, obtenemos los datos del formulario
    if request.method == "POST":
        datosFormulario = request.POST

    # Creamos el formulario con los datos, y si es un POST, llenamos con los datos de la promoción
    form = PromocionForm(datosFormulario, instance=promocion)

    # Si el método es POST y el formulario es válido
    if request.method == "POST":
        if form.is_valid():
            try:
                # Guardamos los cambios del formulario
                form.save()
                
                # Mostramos un mensaje de éxito
                messages.success(request, f"Se ha actualizado la promoción {form.cleaned_data.get('nombre')} correctamente")
                
                # Redirigimos al usuario a la lista de promociones
                return redirect('listar_promociones')
            
            except Exception as error:
                print(error)  # En un entorno real, deberíamos loguear esto o manejarlo en la interfaz
        else:
            print("Errores del formulario:", form.errors)

    # Renderizamos el formulario en caso de GET o si el formulario no es válido
    return render(request, 'formularios/actualizar_promocion.html', {'form': form, 'promocion': promocion})


########################################################################################################################################################################

################################################################        AQUÍ COMIENZAN LOS DELETE      #################################################################

@permission_required('viajes.eliminar_usuario')
def eliminar_usuario(request,usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    try:
        usuario.delete()
        messages.success(request, "Se ha elimnado el usuario "+usuario.nombre+" correctamente")
    except Exception as error:
        print(error)
    return redirect('listar_usuarios')



@permission_required('viajes.eliminar_reserva')
def eliminar_reserva(request,reserva_id):
    reserva = Reserva.objects.get(id=reserva_id)
    try:
        reserva.delete()
        messages.success(request, "Se ha elimnado la reserva "+reserva.codigo_reserva+" correctamente")
    except Exception as error:
        print(error)
    return redirect('listar_reservas')


@permission_required('viajes.eliminar_destino')
def eliminar_destino(request,destino_id):
    destino = Destino.objects.get(id=destino_id)
    try:
        destino.delete()
        messages.success(request, "Se ha elimnado el destino "+destino.nombre+" correctamente")
    except Exception as error:
        print(error)
    return redirect('listar_destinos')



@login_required
def eliminar_alojamiento(request,alojamiento_id):
    alojamiento = Alojamiento.objects.get(id=alojamiento_id)
    try:
        alojamiento.delete()
        messages.success(request, "Se ha elimnado el alojamiento "+alojamiento.nombre+" correctamente")
    except Exception as error:
        print(error)
    return redirect('listar_alojamientos')



@permission_required('viajes.eliminar_comentario')
def eliminar_comentario(request,comentario_id):
    comentario = Comentario.objects.get(id=comentario_id)
    try:
        comentario.delete()
        messages.success(request, "Se ha elimnado el comentario "+comentario.titulo+" correctamente")
    except Exception as error:
        print(error)
    return redirect('listar_comentarios')



@login_required
def eliminar_promocion(request,promocion_id):
    promocion = Promocion.objects.get(id=promocion_id)
    try:
        promocion.delete()
        messages.success(request, "Se ha elimnado la promocion "+promocion.nombre+" correctamente")
    except Exception as error:
        print(error)
    return redirect('listar_promociones')


########################################################################################################################################################################


def registrar_usuario(request):
    if request.method == 'POST':
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            user = formulario.save()
            rol = int(formulario.cleaned_data.get('rol'))
            user.user_permissions.clear()
            
            if(rol == Usuario.CLIENTE):
                grupo = Group.objects.get(name='Clientes')
                grupo.user_set.add(user)
                cliente = Cliente.objects.create(usuario = user)
                cliente.save()
                
            elif(rol == Usuario.PROVEEDOR):
                grupo = Group.objects.get(name='Proveedores')
                grupo.user_set.add(user)
                
                empresa = formulario.cleaned_data.get('empresa')
                rating = formulario.cleaned_data.get('rating')
                
                proveedor = Proveedor.objects.create(usuario = user, empresa = empresa, rating = rating)
                proveedor.save()

            login(request, user)
            return redirect('index')
    else:
        formulario = RegistroForm()
    return render(request, 'registration/signup.html', {'formulario': formulario})


########################################################################################################################################################################


#Ahora vamos a crear las 4 páginas de error
def error_404_view(request, exception=None):
    return render(request, 'errores/404.html', None, None, 404)

def error_403_view(request, exception=None):
    return render(request, 'errores/403.html', None, None, 403)

def error_400_view(request, exception=None):
    return render(request, 'errores/400.html', None, None, 400)

def error_500_view(request, exception=None):
    return render(request, 'errores/500.html', None, None,500)
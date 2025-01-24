from django.contrib import admin

# Register your models here.

from .models import Usuario
from .models import Destino
from .models import Alojamiento
from .models import Reserva
from .models import Comentario
from .models import Extra
from .models import Pasaporte
from .models import Transporte
from .models import Promocion
from .models import Factura

admin.site.register(Usuario)
admin.site.register(Destino)
admin.site.register(Alojamiento)
admin.site.register(Reserva)
admin.site.register(Comentario)
admin.site.register(Extra)
admin.site.register(Pasaporte)
admin.site.register(Transporte)
admin.site.register(Promocion)
admin.site.register(Factura)
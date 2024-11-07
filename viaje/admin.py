# viaje/admin.py
from django.contrib import admin
from .models import EstadoViaje, Viaje, Ruta, ViajeColaborador, EstadoAlojamiento, Alojamiento, AlojamientoAsignacion

admin.site.register(EstadoViaje)
admin.site.register(Viaje)
admin.site.register(Ruta)
admin.site.register(ViajeColaborador)
admin.site.register(EstadoAlojamiento)
admin.site.register(Alojamiento)
admin.site.register(AlojamientoAsignacion)

# viaje/models.py
from django.db import models

class EstadoViaje(models.Model):
    nombre_estado = models.CharField(max_length=50)

class Viaje(models.Model):
    fecha_viaje = models.DateField()
    vehiculo_id_externo = models.CharField(max_length=255)
    vehiculo_patente = models.CharField(max_length=50)
    conductor_id_externo = models.CharField(max_length=255)
    conductor_nombre = models.CharField(max_length=255)
    id_estado = models.ForeignKey(EstadoViaje, on_delete=models.CASCADE, related_name='viajes')

class Ruta(models.Model):
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE, related_name='rutaviaje')
    direccion_origen = models.CharField(max_length=255)
    direccion_destino = models.CharField(max_length=255)
    orden_ruta = models.IntegerField()

class ViajeColaborador(models.Model):
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE, related_name='viajes_colaboradores')
    colaborador_id_externo = models.CharField(max_length=255)
    colaborador_nombre = models.CharField(max_length=255)

class EstadoAlojamiento(models.Model):
    nombre_estado = models.CharField(max_length=50)

class Alojamiento(models.Model):
    nombre = models.CharField(max_length=100)
    capacidad = models.IntegerField()
    estado = models.ForeignKey(EstadoAlojamiento, on_delete=models.SET_NULL, null=True, related_name='alojamientos')

class AlojamientoAsignacion(models.Model):
    alojamiento = models.ForeignKey(Alojamiento, on_delete=models.CASCADE, related_name='asignaciones')
    colaborador_id_externo = models.CharField(max_length=255)
    colaborador_nombre = models.CharField(max_length=255)
    fecha_ingreso = models.DateField()
    fecha_salida = models.DateField()

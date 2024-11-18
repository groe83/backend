# viaje/models.py
from django.db import models
from django.conf import settings


from django.db import models


class EstadoViaje(models.Model):
    nombre_estado = models.CharField(max_length=50)

    class Meta:
        db_table = 'viajes_estadoviaje'  # Nombre exacto de la tabla en la base de datos
        managed = False  # No permite que Django gestione esta tabla


class Ruta(models.Model):
    descripcion_ruta = models.CharField(max_length=255)
    punto_inicial_latitud = models.DecimalField(max_digits=25, decimal_places=15)
    punto_inicial_longitud = models.DecimalField(max_digits=25, decimal_places=15)
    punto_final_latitud = models.DecimalField(max_digits=25, decimal_places=15)
    punto_final_longitud = models.DecimalField(max_digits=25, decimal_places=15)

    class Meta:
        db_table = 'viajes_ruta'
        managed = False


class Viaje(models.Model):
    codigo_viaje = models.CharField(max_length=50)  
    fecha_salida = models.DateField()
    hora_salida = models.TimeField()
    fecha_creacion = models.DateTimeField(null=True, blank=True)
    fecha_modificacion = models.DateTimeField(null=True, blank=True)
    punto_partida = models.CharField(max_length=255, null=True, blank=True)
    punto_destino = models.CharField(max_length=255, null=True, blank=True)
    numero_pasajeros = models.IntegerField(null=True, blank=True)
    kilometros = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    valor_estimado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estado_inicio_real = models.TimeField(null=True, blank=True)
    estado_fin_real = models.TimeField(null=True, blank=True)
    motivo_cancelacion = models.CharField(max_length=255, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    id_viaje_anterior = models.BigIntegerField(null=True, blank=True)
    tarifa_base = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    peajes = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tarifa_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    confirmado_por_conductor = models.BooleanField()
    id_ruta = models.ForeignKey('Ruta', on_delete=models.DO_NOTHING, db_column='id_ruta_id', null=True, blank=True)
    tiempo_estimado = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'viajes_viaje'
        managed = False


class ViajeColaborador(models.Model):
    rut_colaborador = models.CharField(max_length=255)  # Campo ajustado al CSV
    id_viaje = models.ForeignKey('Viaje', on_delete=models.CASCADE, db_column='id_viaje')  # Relación con 'viajes_viaje'
    hora_asignacion = models.DateTimeField(null=True, blank=True)
    id_estado = models.IntegerField(null=True, blank=True)
    qr_escaneado = models.BooleanField(default=False)
    qr_generado = models.BooleanField(default=False)

    class Meta:
        db_table = 'viajes_viajecolaborador'
        managed = False
        unique_together = ('rut_colaborador', 'id_viaje')


class LogEscaneoQR(models.Model):
    fecha_hora_escaneo = models.DateTimeField()
    resultado = models.CharField(max_length=255)
    colaborador_id = models.ForeignKey('ViajeColaborador', on_delete=models.SET_NULL, db_column='colaborador_id', null=True, blank=True)
    conductor_id = models.BigIntegerField(null=True, blank=True)
    viaje_id = models.ForeignKey('Viaje', on_delete=models.CASCADE, db_column='viaje_id')

    class Meta:
        db_table = 'viajes_logescaneoqr'
        managed = False


class RutaViaje(models.Model):
    id_viaje = models.ForeignKey('Viaje', on_delete=models.CASCADE, db_column='id_viaje_id')  # Relación con 'viajes_viaje'
    latitud = models.DecimalField(max_digits=25, decimal_places=15)
    longitud = models.DecimalField(max_digits=25, decimal_places=15)
    orden = models.IntegerField(null=True, blank=True)
    hora_estimada_recogida = models.TimeField(null=True, blank=True)
    hora_real_llegada = models.TimeField(null=True, blank=True)
    hora_real_recogida = models.TimeField(null=True, blank=True)

    class Meta:
        db_table = 'viajes_rutaviaje'
        managed = False

# Modelo para campamentero_asignacionhabitacion
class AsignacionHabitacion(models.Model):
    hora_ingreso = models.TimeField()
    fecha_ingreso = models.DateField()
    fecha_salida = models.DateField()
    rut_colaborador_id = models.CharField(max_length=12)
    id_habitacion_id = models.BigIntegerField()  # Ajuste al campo de clave foránea
    fecha_real_ingreso = models.DateField(null=True, blank=True)
    fecha_real_salida = models.DateField(null=True, blank=True)
    hora_real_ingreso = models.DateTimeField(null=True, blank=True)
    hora_salida = models.TimeField()
    hora_real_salida = models.DateTimeField(null=True, blank=True)
    estado_reserva_id = models.BigIntegerField()  # Ajuste al campo de clave foránea

    class Meta:
        db_table = 'campamentero_asignacionhabitacion'

# Modelo para campamentero_comentariocalidadhabitacion
class ComentarioCalidadHabitacion(models.Model):
    calidad = models.IntegerField()
    comentario = models.TextField(null=True, blank=True)
    fecha = models.DateTimeField()
    asignacion_habitacion = models.BigIntegerField()
    colaborador_id = models.CharField(max_length=12)

    class Meta:
        db_table = 'campamentero_comentariocalidadhabitacion'

# Modelo para campamentero_habitacion
class Habitacion(models.Model):
    nro_habitacion = models.IntegerField()
    ubicacion_id = models.BigIntegerField()
    estado_id = models.BigIntegerField()

    class Meta:
        db_table = 'campamentero_habitacion'

# Modelo para campamentero_logescaneoqrhabitacion
class LogEscaneoQRHabitacion(models.Model):
    fecha_hora_escaneo = models.DateTimeField()
    resultado = models.CharField(max_length=50)
    asignacion_habitacion = models.BigIntegerField()
    colaborador_id = models.CharField(max_length=12)
    encargado_id = models.CharField(max_length=12)
    ciudad = models.CharField(max_length=100, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    pais = models.CharField(max_length=100, null=True, blank=True)
    tipo = models.CharField(max_length=10)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'campamentero_logescaneoqrhabitacion'

# Modelo para campamentero_ubicacion
class Ubicacion(models.Model):
    nombre = models.CharField(max_length=255)

    class Meta:
        db_table = 'campamentero_ubicacion'

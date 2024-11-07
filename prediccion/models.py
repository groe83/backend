from django.db import models

# Create your models here.
# prediccion/models.py


class PrediccionTiempoTraslado(models.Model):
    fecha_prediccion = models.DateField(auto_now_add=True)
    tiempo_estimado = models.FloatField()
    modelo_utilizado = models.CharField(max_length=50)

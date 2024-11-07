# prediccion/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('predecir-tiempo-traslado/', views.predecir_tiempo_traslado, name='predecir_tiempo_traslado'),
    path('predecir-demanda-alojamiento/', views.predecir_demanda_alojamiento, name='predecir_demanda_alojamiento'),
]

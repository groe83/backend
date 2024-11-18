from django.urls import path
from . import views
#from .views import PrediccionTiempoTrasladoAPIView, DatosHistoricosAPIView

urlpatterns = [
    path('', views.home, name='home'),
    path('predecir-tiempo-traslado/', views.predecir_tiempo_traslado, name='predecir_tiempo_traslado'),
    #path('historico-tiempo-traslado/', views.obtener_datos_historicos_tiempo_traslado, name='historico_tiempo_traslado'),
    path('predecir-demanda-semanal/', views.predecir_demanda_semanal, name='predecir_demanda_semanal'),

    #path('prediccion-tiempo-traslado/', PrediccionTiempoTrasladoAPIView.as_view(), name='prediccion-tiempo-traslado'),
    #path('datos-historicos-tiempo-traslado/', DatosHistoricosAPIView.as_view(), name='datos-historicos-tiempo-traslado'),
]

# prediccion/views.py
from django.http import JsonResponse
from .modelo_prediccion import ModeloTiempoTraslado, ModeloDemandaAlojamiento
import pandas as pd
from viaje.models import Viaje, Ruta, ViajeColaborador
from django.http import HttpResponse
import logging

# Configura el logger
logger = logging.getLogger(__name__)

def home(request):
    return HttpResponse("Bienvenido a la API de Modelos Predictivos")


def predecir_tiempo_traslado(request):
    try:
        # Cargar los datos de la base de datos en el DataFrame
        viajes = Viaje.objects.select_related('rutaviaje').values(
            'fecha_viaje', 'vehiculo_id_externo', 'conductor_id_externo', 
            'rutaviaje__direccion_origen', 'rutaviaje__direccion_destino', 'rutaviaje__orden_ruta'
        )
        print(viajes)

        # Crear el DataFrame solo si se obtienen resultados
        if viajes:
            datos_df = pd.DataFrame(viajes)
        else:
        
            return JsonResponse({"error": "No hay datos disponibles para realizar la predicción."}, status=404)

        # Crear y entrenar el modelo de predicción de tiempo de traslado
        modelo = ModeloTiempoTraslado(datos_df)
        modelo.entrenar_modelo()
        
        # Generar predicciones basadas en los datos obtenidos de la base de datos
        prediccion = modelo.predecir(datos_df)
        return JsonResponse({"tiempo_estimado": prediccion.tolist()})
    except Exception as e:
        # Captura el tipo y el mensaje de error
        error_message = str(e)
        logger.error(f"Error al obtener los datos de la base de datos: {error_message}")
        
        # Devuelve una respuesta con el mensaje de error
        return JsonResponse({"error": "Error al obtener datos de la base de datos", "detalle": error_message}, status=500)
    
    
def predecir_demanda_alojamiento(request):
    # Obtener los datos necesarios de la base de datos y verificar que los campos estén correctos
    alojamiento = ViajeColaborador.objects.select_related('viaje').values(
        'viaje__fecha_viaje'  # Asegúrate de que el campo `fecha_viaje` esté correctamente definido en `Viaje`
    )
    
    # Crear el DataFrame solo si hay resultados en la consulta
    if alojamiento:
        datos_df = pd.DataFrame(alojamiento)
    else:
        return JsonResponse({"error": "No hay datos disponibles para realizar la predicción de demanda de alojamiento."}, status=404)

    # Crear y entrenar el modelo de predicción de demanda de alojamiento
    modelo = ModeloDemandaAlojamiento(datos_df)
    modelo.entrenar_arima()
    
    # Generar predicciones para la demanda futura de alojamiento
    predicciones = modelo.predecir_arima()
    return JsonResponse({"demanda_estimada": predicciones.tolist()})
# prediccion/views.py
from django.http import JsonResponse, HttpResponse
from .modelo_prediccion import ModeloTiempoTraslado, ModeloDemandaAlojamiento
import pandas as pd
import logging
from viaje.models import AsignacionHabitacion, Viaje, Ruta
from datetime import datetime, timedelta
from django.db.models import Avg, F
from django.db import models
import math
from prophet import Prophet

# Configura el logger
logger = logging.getLogger(__name__)

def home(request): 
    return HttpResponse("Bienvenido a la API de Modelos Predictivos")

def predecir_tiempo_traslado(request):
    try:
        # Obtener datos históricos desde enero de 2023 hasta noviembre de 2024
        fecha_inicio_historica = datetime(2023, 1, 1)
        fecha_fin_historica = datetime(2024, 11, 30)
        viajes = Viaje.objects.filter(fecha_salida__range=[fecha_inicio_historica, fecha_fin_historica]) \
            .values('fecha_salida', 'tiempo_estimado')

        if not viajes:
            return JsonResponse({"error": "No hay datos históricos disponibles para realizar la predicción."}, status=404)

        # Crear DataFrame a partir de los datos históricos
        datos_df = pd.DataFrame(viajes)
        datos_df['fecha_salida'] = pd.to_datetime(datos_df['fecha_salida'])

        # Validar y convertir `tiempo_estimado` a numérico
        datos_df['tiempo_estimado'] = pd.to_numeric(datos_df['tiempo_estimado'], errors='coerce')

        # Filtrar valores no numéricos o nulos
        datos_df = datos_df.dropna(subset=['tiempo_estimado'])

        # Asegurarse de que la columna 'tiempo_estimado' está en formato numérico
        datos_df['tiempo_estimado'] = datos_df['tiempo_estimado'].astype(float)

        # Crear la columna de meses
        datos_df['mes'] = datos_df['fecha_salida'].dt.to_period('M')

        # Calcular el promedio mensual de tiempo de traslado
        historico_mensual = datos_df.groupby('mes').agg({'tiempo_estimado': 'mean'}).reset_index()
        historico_mensual.rename(columns={'mes': 'ds', 'tiempo_estimado': 'y'}, inplace=True)

        # Convertir a formato necesario
        historico_mensual['ds'] = historico_mensual['ds'].astype(str)  # Convertir períodos a cadenas
        historico_mensual['y'] = historico_mensual['y'].round()

        # Agregar columna `y_horas`
        historico_mensual['y_horas'] = historico_mensual['y'].apply(lambda minutos: f"{int(minutos // 60)}h {int(minutos % 60)}m")

        # Promedio histórico por mes
        promedio_estacional = historico_mensual.groupby(historico_mensual['ds'].str[-2:]).agg({'y': 'mean'}).reset_index()
        promedio_estacional.rename(columns={'ds': 'mes', 'y': 'y_estacional'}, inplace=True)
        promedio_estacional['mes'] = promedio_estacional['mes'].astype(str)

        # Entrenar modelo Prophet
        modelo = Prophet()
        # Convertir `ds` nuevamente a timestamp para Prophet
        historico_mensual['ds'] = pd.to_datetime(historico_mensual['ds'])
        modelo.fit(historico_mensual[['ds', 'y']])

        # Generar predicciones para diciembre 2024 y enero-junio 2025
        future = modelo.make_future_dataframe(periods=8, freq='M')
        forecast = modelo.predict(future)

        # Filtrar predicciones para diciembre 2024 y enero-junio 2025
        predicciones = forecast[(forecast['ds'] >= "2024-12-01") & (forecast['ds'] <= "2025-07-30")]
        predicciones['yhat'] = predicciones['yhat'].round()

        # Predicciones basándose en los datos históricos
        predicciones['mes'] = predicciones['ds'].dt.month.astype(str).str.zfill(2)
        predicciones = pd.merge(predicciones, promedio_estacional, left_on='mes', right_on='mes', how='left')
        predicciones['y_ajustada'] = (predicciones['yhat'] * 0.6 + predicciones['y_estacional'] * 0.4).round()

        # Formatear resultados
        predicciones['y_horas'] = predicciones['y_ajustada'].apply(lambda minutos: f"{int(minutos // 60)}h {int(minutos % 60)}m")
        predicciones['ds'] = predicciones['ds'].dt.to_period('M').astype(str)
        predicciones = predicciones[['ds', 'y_ajustada', 'y_horas']].rename(columns={'y_ajustada': 'y'})

        # Formatear datos históricos
        historico_mensual['ds'] = historico_mensual['ds'].dt.to_period('M').astype(str)
        historico_mensual = historico_mensual[['ds', 'y', 'y_horas']]

        return JsonResponse({
            "historico_tiempo_traslado_mensual": historico_mensual.to_dict(orient='records'),
            "prediccion_tiempo_traslado_mensual": predicciones.to_dict(orient='records')
        })

    except Exception as e:
        error_message = str(e)
        return JsonResponse({"error": "Error al obtener los datos de la base de datos", "detalle": error_message}, status=500)



#Predicción Demanda de Habitaciones y Datos Historicos

def predecir_demanda_semanal(request):
    #def calcular_y_predecir_demanda_habitaciones(request):
    try:
        # Definir el inicio del período histórico desde enero de 2023
        inicio_periodo_historial = datetime(year=2023, month=1, day=1)

        # Extraer los datos de las reservas históricas desde enero de 2023
        ocupaciones = AsignacionHabitacion.objects.filter(
            fecha_ingreso__gte=inicio_periodo_historial,
            estado_reserva_id__gt=1
        ).values('fecha_ingreso', 'fecha_salida', 'id_habitacion_id')

        if not ocupaciones:
            return JsonResponse({
                "error": "No hay datos históricos suficientes para realizar la predicción de ocupación de alojamiento."
            }, status=404)

        # Crear DataFrame y expandir el rango de fechas
        ocupaciones_df = pd.DataFrame(list(ocupaciones))
        ocupaciones_df['fecha_ingreso'] = pd.to_datetime(ocupaciones_df['fecha_ingreso'])
        ocupaciones_df['fecha_salida'] = pd.to_datetime(ocupaciones_df['fecha_salida'])

        # Generar una columna de rango de fechas de ocupación para cada estancia
        fechas_expandida = ocupaciones_df.apply(lambda row: pd.date_range(row['fecha_ingreso'], row['fecha_salida'], freq='D'), axis=1)
        ocupaciones_df = ocupaciones_df.loc[ocupaciones_df.index.repeat(fechas_expandida.str.len())]
        ocupaciones_df['fecha_ocupacion'] = fechas_expandida.explode().values

        # Eliminar duplicados para cada `id_habitacion_id` en la misma fecha de ocupación
        ocupaciones_df = ocupaciones_df.drop_duplicates(subset=['fecha_ocupacion', 'id_habitacion_id'])

        # Calcular la ocupación diaria
        ocupacion_diaria = ocupaciones_df.groupby('fecha_ocupacion').size().reset_index(name='habitaciones_ocupadas')
        ocupacion_diaria['habitaciones_ocupadas'] = ocupacion_diaria['habitaciones_ocupadas'].apply(math.ceil)  # Redondeo de históricos
        ocupacion_diaria['mes'] = ocupacion_diaria['fecha_ocupacion'].dt.to_period('M')

        # Seleccionar la mediana de ocupación mensual y redondear
        ocupacion_mensual = ocupacion_diaria.groupby('mes')['habitaciones_ocupadas'].median().reset_index()
        ocupacion_mensual['habitaciones_ocupadas'] = ocupacion_mensual['habitaciones_ocupadas'].apply(math.ceil)
        ocupacion_mensual['mes'] = ocupacion_mensual['mes'].astype(str)

        # Preparar datos para Prophet
        ocupaciones_df_historial = ocupacion_diaria[['fecha_ocupacion', 'habitaciones_ocupadas']].copy()
        ocupaciones_df_historial = ocupaciones_df_historial.rename(columns={'fecha_ocupacion': 'ds', 'habitaciones_ocupadas': 'y'})

        # Crear y entrenar el modelo Prophet con ajustes
        modelo = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
        modelo.add_seasonality(name='monthly', period=30.5, fourier_order=5)
        modelo.fit(ocupaciones_df_historial)

        # Predecir para los próximos meses a partir de diciembre de 2024
        future_dates = modelo.make_future_dataframe(periods=210, freq='D')
        forecast = modelo.predict(future_dates)
        forecast['mes'] = forecast['ds'].dt.to_period('M')
        prediccion_mensual = forecast.groupby('mes')['yhat'].median().reset_index()  # Usar mediana para suavizar predicción
        prediccion_mensual['yhat'] = prediccion_mensual['yhat'].apply(math.ceil)  # Redondear al entero superior
        prediccion_mensual = prediccion_mensual[prediccion_mensual['mes'] >= '2024-12']  # Desde diciembre 2024 en adelante

        # Convertir a formato JSON amigable
 
        prediccion_mensual['mes'] = prediccion_mensual['mes'].astype(str)
        prediccion_mensual_dict = [{"mes": row['mes'], "prediccion": row['yhat']} for _, row in prediccion_mensual.iterrows()]

        return JsonResponse({
            "ocupacion_mensual_historica": ocupacion_mensual.to_dict(orient='records'),
            "prediccion_mensual": prediccion_mensual_dict
        })

    except Exception as e:
        error_message = str(e)
        return JsonResponse({
            "error": "Error al obtener los datos de la base de datos",
            "detalle": error_message
        }, status=500)
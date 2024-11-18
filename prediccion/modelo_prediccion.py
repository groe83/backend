import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import GradientBoostingRegressor
from prophet import Prophet
from datetime import datetime, timedelta
from viaje.models import Viaje


class ModeloDemandaAlojamiento:
    def __init__(self, df=None):
        self.model_prophet = None
        self.df_historico = None
        if df is not None:
            self.df_historico = df[['ds', 'y']].copy()

    def entrenar_prophet(self, df):
        """
        Entrena el modelo Prophet utilizando los datos históricos proporcionados.
        """
        self.df_historico = df[['ds', 'y']].copy()

        # Configuración del modelo Prophet
        self.model_prophet = Prophet(yearly_seasonality=True, weekly_seasonality=True)
        self.model_prophet.add_seasonality(name='monthly', period=30.5, fourier_order=5)
        self.model_prophet.fit(self.df_historico)

    def predecir_prophet(self, periods=30):
        """
        Genera predicciones para el número de períodos especificados (por defecto 30 días).
        """
        future_dates = self.model_prophet.make_future_dataframe(periods=periods)
        forecast = self.model_prophet.predict(future_dates)
        return forecast[['ds', 'yhat']]

    def generar_alerta(self, demanda_estimada, fecha_objetivo):
        """
        Genera una alerta si la demanda estimada supera el 20% del promedio del año anterior.
        """
        fecha_objetivo = pd.Timestamp(fecha_objetivo)
        fecha_inicio_anterior = fecha_objetivo - timedelta(days=365)

        # Filtrar los datos históricos del mismo mes en el año anterior
        df_anterior = self.df_historico[
            (pd.to_datetime(self.df_historico['ds']) >= fecha_inicio_anterior) &
            (pd.to_datetime(self.df_historico['ds']) <= fecha_objetivo)
        ]

        if df_anterior.empty:
            return "Sin datos para el año anterior."

        promedio_anno_anterior = df_anterior['y'].mean()
        if demanda_estimada > 1.2 * promedio_anno_anterior:
            return f"Alerta: La demanda estimada es un 20% superior al promedio del mismo mes del año anterior ({promedio_anno_anterior:.0f})."

        return "La demanda estimada está dentro del rango esperado."


class ModeloTiempoTraslado:
    def __init__(self):
        self.model_prophet = None

    def entrenar_prophet(self, df):
        # Guardar los datos históricos
        self.df_historico = df[['ds', 'y']].copy()

        # Crear y entrenar el modelo Prophet
        self.model_prophet = Prophet(yearly_seasonality=True, weekly_seasonality=True)
        self.model_prophet.fit(self.df_historico)

    def predecir_prophet(self, periods=7):
        # Crear un rango futuro de fechas
        future_dates = self.model_prophet.make_future_dataframe(periods=periods, freq='W')
        forecast = self.model_prophet.predict(future_dates)
        return forecast[['ds', 'yhat']]
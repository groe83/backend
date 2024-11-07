# prediccion/models_prediccion.py
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
import xgboost as xgb
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet

class ModeloTiempoTraslado:
    def __init__(self, df):
        self.df = df
    
    def entrenar_modelo(self):
        X = self.df[['fecha_viaje', 'vehiculo_id_externo', 'conductor_id_externo', 'direccion_origen', 'direccion_destino', 'orden_ruta']]
        y = self.df['tiempo_estimado_traslado']
        
        poly_model = PolynomialFeatures(degree=2)
        X_poly = poly_model.fit_transform(X)
        
        # Modelo Gradient Boosting
        self.model = GradientBoostingRegressor()
        self.model.fit(X_poly, y)
    
    def predecir(self, nuevos_datos):
        nuevos_datos_poly = PolynomialFeatures(degree=2).fit_transform(nuevos_datos)
        return self.model.predict(nuevos_datos_poly)


class ModeloDemandaAlojamiento:
    def __init__(self, df):
        self.df = df
    
    def entrenar_arima(self):
        y = self.df.set_index('fecha_viaje')['ocupacion_alojamiento']
        arima_model = ARIMA(y, order=(1, 1, 1))
        self.model_arima = arima_model.fit()

    def predecir_arima(self, steps=30):
        return self.model_arima.forecast(steps=steps)

    def entrenar_prophet(self):
        df_prophet = self.df.rename(columns={'fecha_viaje': 'ds', 'ocupacion_alojamiento': 'y'})
        self.model_prophet = Prophet(yearly_seasonality=True)
        self.model_prophet.fit(df_prophet)

    def predecir_prophet(self, periods=30):
        future_dates = self.model_prophet.make_future_dataframe(periods=periods)
        forecast = self.model_prophet.predict(future_dates)
        return forecast[['ds', 'yhat']]

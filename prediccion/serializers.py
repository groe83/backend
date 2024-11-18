from rest_framework import serializers
from rest_framework import serializers
from .models import Viaje, LogEscaneoQR, RutaViaje, ViajeColaborador

class TimePredictionSerializer(serializers.Serializer):
    date = serializers.DateField()
    predicted_time = serializers.FloatField()

class DemandPredictionSerializer(serializers.Serializer):
    date = serializers.DateField()
    predicted_demand = serializers.FloatField()


class ViajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viaje
        fields = '__all__'

class LogEscaneoQRSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEscaneoQR
        fields = '__all__'

class RutaViajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RutaViaje
        fields = '__all__'

class ViajeColaboradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViajeColaborador
        fields = '__all__'
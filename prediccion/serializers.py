from rest_framework import serializers

class TimePredictionSerializer(serializers.Serializer):
    date = serializers.DateField()
    predicted_time = serializers.FloatField()

class DemandPredictionSerializer(serializers.Serializer):
    date = serializers.DateField()
    predicted_demand = serializers.FloatField()

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from publisher.models import Measurement
from publisher.models import Bus
from publisher.models import Stop
from datetime import datetime

class MeasurementSerializer (serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ('created_on', 'bus', 'stop', 'time', 'lat', 'lng', 'temperature', 'humidity', 'light', 'rain')

class MeasurementBatchSerializer (serializers.Serializer):
    node_id=serializers.IntegerField()
    received= serializers.DateTimeField(input_formats=['%d%m%y%H%M%S00'])
    header= serializers.CharField()
    load=serializers.ListField(child= serializers.CharField())
    m_list = []

    def create(self, validated_data):
        column_names = validated_data["header"].split(",")

        b = Bus.objects.get(pk=validated_data["node_id"])
        s = Stop.objects.get(pk=validated_data["stop_id"])

        for l in validated_data["load"]:
            data=l.split(",")
            m = Measurement.objects.create(
            stop = s,
            bus = b,
            time = datetime.strptime(data[column_names.index("datetime")],'%d%m%y%H%M%S00'),
            lat = data[column_names.index("lat")],
            lng = data[column_names.index("lng")],
            temperature = data[column_names.index("light")],
            humidity = data[column_names.index("temperature")],
            light = data[column_names.index("humidity")],
            rain = data[column_names.index("rain")])
            self.m_list.append(m)
        return validated_data
    
    def save(self):
        for m in self.m_list:
            m.save()
        return
        
    def update(self, instance, validated_data):
        return instance

class MeasurementBatchList (serializers.Serializer):
    stop_id=serializers.IntegerField()
    batch=ListField(child= MeasurementBatchSerializer())

class DataSerializer(serializers.Serializer):
    data = serializers.ListField(child= MeasurementSerializer())

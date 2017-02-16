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
    serialized_stop = 0

    def create(self, validated_data):
        print "Creating batch"
        column_names = validated_data["header"].split(",")

        b = Bus.objects.get(pk=validated_data["node_id"])

        for l in validated_data["load"]:
            data=l.split(",")
            m = {}#Measurement.objects.create(
            m['bus'] = b,
            m['time'] = datetime.strptime(data[column_names.index("datetime")],'%d%m%y%H%M%S00')
            m['lat'] = data[column_names.index("lat")]
            m['lng'] = data[column_names.index("lng")]
            m['temperature'] = data[column_names.index("light")]
            m['humidity'] = data[column_names.index("temperature")]
            m['light'] = data[column_names.index("humidity")]
            m['rain'] = data[column_names.index("rain")]
            self.m_list.append(m)
        return validated_data
    
    def save(self):
        for m in self.m_list:
            measurement = Measurement.objects.create(
                stop = self.serialized_stop,
                bus = m['bus'],
                time = m['time'],
                lat = m['lat'],
                lng = m['lng'],
                temperature = m['temperature'],
                humidity = m['humidity'],
                light = m['light'],
                rain = m['rain'],
            )
            measurement.save()
        return
        
    def update(self, instance, validated_data):
        return instance


class MeasurementBatchList (serializers.Serializer):
    """This method receives data directly from the Raspberries"""
    stop_id = serializers.IntegerField()
    batches = serializers.ListField(child=MeasurementBatchSerializer())

    def create(self, validated_data):
        s = Stop.objects.get(pk=validated_data["stop_id"])
        print validated_data
        for batch in validated_data['batches']:
            column_names = batch["header"].split(",")
            b = Bus.objects.get(pk=batch["node_id"])
            for l in batch["load"]:
                data=l.split(",")
                m = Measurement.objects.create(
                bus = b,
                stop = s,
                time = datetime.strptime(data[column_names.index("datetime")],
                                        '%d%m%y%H%M%S00'),
                lat = data[column_names.index("lat")],
                lng = data[column_names.index("lng")],
                temperature = data[column_names.index("light")],
                humidity = data[column_names.index("temperature")],
                light = data[column_names.index("humidity")],
                rain = data[column_names.index("rain")])
                m.save()
        return validated_data

class DataSerializer(serializers.Serializer):
    data = serializers.ListField(child=MeasurementSerializer())

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from publisher.models import Measurement

class MeasurementSerializer (serializers.ModelSerializer):
    class Meta:
	model = Measurement
        fields = ('created_on', 'bus', 'stop', 'time', 'lat', 'lng', 'temperature', 'humidity', 'light', 'rain')
    
class dataSerializer(serializers.Serializer):
        data = serializers.ListField(child= MeasurementSerializer())

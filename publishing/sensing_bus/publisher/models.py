from django.db import models
from djangotoolbox.fields import EmbeddedModelField

class Location(models.Model):
    """Represents a point in latitude and longitude"""
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)

class Bus(models.Model):
    """Represents a bus carrying a sensor node"""
    name = models.CharField(max_length=10)

class Stop(model.Model):
    """Represents a bus stop having a flushing node"""
    location = EmbeddedModelField('Location')

class Context(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    bus = EmbeddedModelField('Bus')
    time = models.DateTimeField()


class Measurement(models.Model):
    """Represents the measurements made by a bus on a given time and place"""
    context = EmbeddedModelField('Context')

    temperature = models.DecimalField(max_digits=4, decimal_places=1)
    humidity = models.DecimalField(max_digits=4, decimal_places=1)
    light = models.DecimalField(max_digits=4, decimal_places=1)
    rain = models.DecimalField(max_digits=4, decimal_places=1)
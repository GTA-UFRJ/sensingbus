from __future__ import unicode_literals
from django.db import models

class Bus(models.Model):
    """Represents a bus carrying a sensor node"""
    name = models.CharField(max_length=10, unique=True)

    def __unicode__(self):
        return self.name

class SensingNode(models.Model):
    """Represents a sensor node, from the Gathering layer"""
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE,
         verbose_name="bus where the node is coupled", null=True)
    def __unicode__(self):
        return "{}, {}".format(self.pk, self.bus.name)

class Stop(models.Model):
    """Represents a bus stop having a flushing node"""
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)

    def __unicode__(self):
        return "{}, {}".format(self.lat, self.lng)


class Measurement(models.Model):
    """Represents the measurements made by a bus on a given time and place"""
    #Context of measurements
    created_on = models.DateTimeField(auto_now_add=True)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE,
             verbose_name="bus that collected measurement", null=True)
    node = models.ForeignKey(SensingNode, on_delete=models.CASCADE,
             verbose_name="node that collected measurement")
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE,
             verbose_name="stop that received measurement")
    time = models.DateTimeField()
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)

    #Measurements
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    humidity = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    light = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    rain = models.DecimalField(max_digits=4, decimal_places=1, null=True)

    def __unicode__(self):
        return "{}, {}, {}, {}".format(self.node, self.bus, self.stop, self.time)
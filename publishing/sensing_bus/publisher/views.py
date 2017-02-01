import json
from django.shortcuts import render
from django.http import HttpResponse
from publisher.models import Measurement
from publisher.models import Bus
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from publisher.serializers import MeasurementSerializer
from publisher.serializers import MeasurementBatchSerializer

import datetime

from .forms import VisualizeForm

def index(request):
    context = {}
    return render(request, 'publisher/index.html', context)

def about(request):
    context = {}
    return render(request, 'publisher/about.html', context)

def visualize(request):
    """Renders the visualization webpage on GET and returns map data on POST"""
    form = VisualizeForm()
    context = {'form': form}

    if request.method == 'GET':
        return render(request, 'publisher/visualize.html', context)
    if request.method == 'POST':
        bus_name = request.POST.get("id_bus_name", "")
        min_lat = request.POST.get("id_min_lat", "")
        max_lat = request.POST.get("id_max_lat", "")
        min_lng = request.POST.get("id_min_lng", "")
        max_lng = request.POST.get("id_max_lng", "")
        start_time = request.POST.get("id_start_time", "")
        end_time = request.POST.get("id_end_time", "")
        sensor_name = request.POST.get("id_sensor_name_0", "")

        q = Measurement.objects.all()

        if bus_name:
            bus_key = Bus.objects.filter(name__iexact=bus_name).first().pk
            q = q.filter(bus=bus_key)
        if min_lat:
            q = q.filter(lat__gte=min_lat)
        if max_lat:
            q = q.filter(lat__lte=max_lat)
        if min_lng:
            q = q.filter(lat__gte=min_lng)
        if max_lng:
            q = q.filter(lat__lte=max_lng)
        if start_time:
            q = q.filter(time__gte=start_time)
        if end_time:
            q = q.filter(time__lte=end_time)

        data = {'data' : []}
        for o in q:
            d = {}
            d['lat'] = float(o.lat)
            d['lng'] = float(o.lng)
            if sensor_name == 'TEMPERATURE':
                d['value'] = float(o.temperature)
            if sensor_name == 'HUMIDITY':
                d['value'] = float(o.humidity)
            if sensor_name == 'LIGHT':
                d['value'] = float(o.light)
            if sensor_name == 'RAIN':
                d['value'] = float(o.rain)
            data['data'].append(d)

        data['max'] = 30
        now = datetime.datetime.now()
        html = "Data = %s" % data
        return JsonResponse(data)

    else:
        html = "<html><body>This is not nice, lek</body></html>"
        return HttpResponse(html)

def docs(request):
    context = {}
    return render(request, 'publisher/docs.html', context)

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def measurement_list(request):
    """
    List all code measurements, or create a new measurement.
    """
    if request.method == 'GET':
        measurements = Measurement.objects.all()
        serializer = MeasurementSerializer(measurements, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MeasurementSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def measurement_detail(request, pk):
    """
    Retrieve, update or delete a code measurement.
    """
    try:
        measurement = Measurement.objects.get(pk=pk)
    except Measurement.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MeasurementSerializer(measurement)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = MeasurementSerializer(measurement, data=data)
        if serializer.is_valid():
            #serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        measurement.delete()
        return HttpResponse(status=204)

@csrf_exempt
def measurement_batch_list(request):
    """
    List all code measurements batches, or create a new measurement batch.
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MeasurementBatchSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)
    else:
        return JSONResponse({'msg':'This endpoint is just for POSTs, lek'},status=400)

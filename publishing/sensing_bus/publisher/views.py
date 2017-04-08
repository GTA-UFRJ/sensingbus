import json
from datetime import datetime
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
from publisher.serializers import MeasurementBatchList

from .forms import VisualizeForm

def index(request):
    context = {}
    return render(request, 'publisher/index.html', context)

def about(request):
    context = {}
    return render(request, 'publisher/about.html', context)

def docs(request):
    context = {}
    return render(request, 'publisher/docs.html', context)

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
            q = q.filter(time__gte=datetime.strptime(start_time,
                                        "%m/%d/%Y %I:%M %p"))
        if end_time:
            q = q.filter(time__lte=datetime.strptime(end_time,
                                        "%m/%d/%Y %I:%M %p"))

        data = {'data' : []}
        values = []
        for o in q:
            d = {}
            d['lat'] = float(o.lat)
            d['lng'] = float(o.lng)            
            d['temperature'] = float(o.temperature)
            d['humidity'] = float(o.humidity)
            d['light'] = float(o.light)
            d['rain'] = float(o.rain)
            if sensor_name == 'TEMPERATURE':
                d['value'] = float(o.temperature)
                values.append(float(o.temperature))
            if sensor_name == 'HUMIDITY':
                d['value'] = float(o.humidity)
                values.append(float(o.humidity))
            if sensor_name == 'LIGHT':
                d['value'] = float(o.light)
                values.append(float(o.light))
            if sensor_name == 'RAIN':
                d['value'] = float(o.rain)
                values.append(float(o.rain))
            data['data'].append(d)


        data['max'] = max(values)
        data['min'] = min(values)
        #now = datetime.now()
        #html = "Data = %s" % data
        return JsonResponse(data)

    else:
        html = "<html><body>This is not nice, lek</body></html>"
        return HttpResponse(html)

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
    get:
    List all code measurements
    """
    if request.method == 'GET':
        bus_name = request.GET.get("bus_name", "")
        node_id = request.GET.get("node_id", "")
        min_lat = request.GET.get("min_lat", "")
        max_lat = request.GET.get("max_lat", "")
        min_lng = request.GET.get("min_lng", "")
        max_lng = request.GET.get("max_lng", "")
        start_time = request.GET.get("start_time", "")
        end_time = request.GET.get("end_time", "")

        q = Measurement.objects.all()

        if bus_name:
            bus_key = Bus.objects.filter(name__iexact=bus_name).first().pk
            q = q.filter(bus=bus_key)
        if node_id:
            q = q.filter(node=node_id)
        if min_lat:
            q = q.filter(lat__gte=min_lat)
        if max_lat:
            q = q.filter(lat__lte=max_lat)
        if min_lng:
            q = q.filter(lat__gte=min_lng)
        if max_lng:
            q = q.filter(lat__lte=max_lng)
        if start_time:
            q = q.filter(time__gte=datetime.strptime(start_time,
                                        "%Y-%m-%dT%H:%M:%S"))
        if end_time:
            q = q.filter(time__lte=datetime.strptime(end_time,
                                        "%Y-%m-%dT%H:%M:%S"))
        serializer = MeasurementSerializer(q, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        html = "<html><body>This is not allowed. Use the url /measurements_batch_sec/ </body></html>"
        return HttpResponse(html)

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
        if serializer.is_valid(raise_exception=True):
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
        serializer = MeasurementBatchList(data=data)
        if serializer.is_valid():
            print "Saving"
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)
    else:
        return JSONResponse({'msg':'This endpoint is just for fun'},status=400)

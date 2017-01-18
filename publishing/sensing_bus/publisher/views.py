from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {}
    return render(request, 'publisher/index.html', context)

def about(request):
    context = {}
    return render(request, 'publisher/about.html', context)

def visualize(request):
    context = {}
    return render(request, 'publisher/visualize.html', context)
    #return render(request, 'publisher/index.html', context)

def docs(request):
    context = {}
    return render(request, 'publisher/docs.html', context)
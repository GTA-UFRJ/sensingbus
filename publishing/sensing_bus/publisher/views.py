from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {}
    #return HttpResponse("This is SensingBus.")
    return render(request, 'publisher/index.html', context)
    #return render(request, 'index.html', context)

def detail(request, question_id):
    context = {}
    return render(request, 'base.html', context)
    #return render(request, 'publisher/index.html', context)
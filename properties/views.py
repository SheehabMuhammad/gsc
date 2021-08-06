from django.http import HttpResponse
from django.shortcuts import render
from .models import Property


def index(request):
    properties = Property.objects.all()
    return render(request, 'index.html',  {'properties': properties})

def urls(request, property_id):
    return HttpResponse(f"You're viewing urls of Property: #{property_id}")
    # return render(request, 'properties/index.html')


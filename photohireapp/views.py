from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
  
def home(request):
    images = Images.objects.all()
    return render(request, 'photohireapp/index.html', {'images':images})

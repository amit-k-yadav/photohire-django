from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
  
def home(request):
    return render(request, 'photohireapp/index.html')

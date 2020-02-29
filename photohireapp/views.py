from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
  
def home(request):
    return render(request, 'photohireapp/index.html')

### Keeping this to upload images. Nothing else
def upload_temp(request):
    if request.method == 'POST': 
        form = ImageForm(request.POST, request.FILES) 
  
        if form.is_valid(): 
            form.save() 
            return redirect('success') 
    else: 
        form = ImageForm() 
    return render(request, 'photohireapp/upload_temp.html', {'form' : form}) 

def hotel_image_view(request): 
  
    if request.method == 'POST': 
        form = HotelForm(request.POST, request.FILES) 
  
        if form.is_valid(): 
            form.save() 
            return redirect('success') 
    else: 
        form = HotelForm() 
    return render(request, 'photohireapp/hotel_image_form.html', {'form' : form}) 
  
  
def success(request): 
    return HttpResponse('successfully uploaded') 

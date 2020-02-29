from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
  
def home(request):
    images = Images.objects.all()
    photographers = Person.objects.filter(is_photographer=True)    
    photographers = list(photographers)

    # sort the users in descending order based on profile_view
    top_photographers = sorted(photographers, 
        key = lambda user: user.profile_views, 
        reverse=True
    )

    # Return all images and only top 3 photographers
    return render(request, 
        'photohireapp/index.html', 
        {'images':images, 'top_photographers':top_photographers[0:3]}
    )


def explore(request):
    return render(request, 
        'photohireapp/expore.html'
    )
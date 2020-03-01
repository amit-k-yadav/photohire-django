from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
import random
  
def home(request):
    images = list(Images.objects.all())
    photographers = list(Person.objects.filter(is_photographer=True))

    # Shuffle lists
    random.shuffle(images)
    random.shuffle(photographers)

    # Get first 3 from the shuffled list
    top_photographers = photographers[0:3]

    # Return all images and only 3 photographers
    return render(request, 
        'photohireapp/index.html', 
        {'images':images, 'top_photographers':top_photographers}
    )


def explore(request):
    images = list(Images.objects.all())
    random.shuffle(images)
    # Get top 10 photographers based on their profile views
    trending_photographers = Person.objects.filter(is_photographer=True).order_by('-profile_views')[:10]
    return render(request, 
        'photohireapp/expore.html',
        {'images':images, 'trending_photographers':trending_photographers}
    )

def signin(request):
    return render(request, 
        'photohireapp/sign-in.html'
    )

def signup(request):
    return render(request, 
        'photohireapp/sign-up.html'
    )

def about(request):
    return render(request, 
        'photohireapp/about.html'
    )

def search(request):
    # Get tag searched by user
    tag=request.GET['search']

    # contains case insensitive value of the query
    tagged_images = Images.objects.filter(tags__tag__icontains=tag)

    # Get all the tags
    all_tags = list(Tags.objects.all())
    random.shuffle(all_tags)

    return render(request,
        'photohireapp/search.html',
        {
            'tagged_images': tagged_images,
            'tag':tag,
            'all_tags': all_tags
        }
    )
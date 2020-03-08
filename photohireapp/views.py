from django.http import HttpResponse
from django.shortcuts import render, redirect,reverse
from .forms import *
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
import random

from django.contrib.auth import logout

def logout_view(request):
    print('logout view called')
    logout(request)
    #return render(request,'photohireapp/logout.html') Option 1
    return redirect('signin')

def user_profile(request):
        print('inside edit profile')
        if request.method=='POST':
            print('inside post' , request.POST,'>>user',request.user.id)
            form= editprofileform(request.POST, instance=request.user)
            if form.is_valid():
                print('form is valid')
                bio=form.cleaned_data['bio']
                user=User.objects.get(id=request.user.id).id
                print('User ' , user)
                print(bio)
                update=Profile.objects.filter(user=user).update(bio=bio)
                print('update ??' , update)
                #form.save()
            else:
                print(form.errors)
        else:
            form=editprofileform(instance=request.user)

        return render(request,'photohireapp/edit_profile.html',{'form':form})
	
def home(request):
    images = list(Images.objects.all())
    photographers = list(Profile.objects.filter(is_photographer=True))

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
    trending_photographers = Profile.objects.filter(is_photographer=True).order_by('-profile_views')[:10]
    return render(request, 
        'photohireapp/expore.html',
        {'images':images, 'trending_photographers':trending_photographers}
    )


@csrf_exempt
def signup(request):
    if request.method=='POST':
        print('inside signup page ' , request.POST)
        form=Tes(request.POST)
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            print('form is valid',form.cleaned_data)
            user =form.save()
            user.refresh_from_db()
            user.profile.first_name=form.cleaned_data.get('first_name')
            user.profile.last_name=form.cleaned_data.get('last_name')
            user.profile.is_photographer=form.cleaned_data.get('is_photographer')
            user.save()
            #user_creation= form.save(commit=False)
            #user_creation.user=request.user.id

            print('##############################')
            print(request.user.id)
            #user_creation.save()
            print('%%%%%%%%%%%%%%')
            #user=form.save()
            #Profile.objects.create(user=user,bio=request.POST.get('bio'),first_name=request.POST.get('first_name'),last_name=request.POST.get('last_name'))
            #print(form.cleaned_data)
            #user.profile.birth_date = form.cleaned_data.get('birth_date') 
            #user.save()
            raw_password = form.cleaned_data.get('password1')
            print(form.cleaned_data)	
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
        else:
            print(form.errors)
	    #Profile.objects.create(first_name=first_name,last_name='lasyt')
        return redirect('/')
    else:
        print('get request called')
        form=UserCreationForm()
        args={'form':form}
        return render(request,"photohireapp/sign-up.html",args)
    return render(request, 
        'photohireapp/sign-in.html'
    )


@csrf_exempt
def signin(request):
    if request.method =='POST':
        print(request.POST)
        form=LoginForm(request.POST)
        if form.is_valid():
            cd =form.cleaned_data
            user=authenticate(username = cd['email'] , password = cd['password'])
            if user:
                if user.is_active:
                    login(request,user)
                    return redirect('/user_profile/'+str(user.id))
                    #return HttpResponse('Logged In Successfully !')
                else:
                    return HttpResponse('Account has been disabled ')
            else:
                return HttpResponse('User does not Exist')
        else:
	        print(form.errors)
    else:
        print('GET login called >>')
        form=LoginForm()
    return render(request , 'photohireapp/sign-in.html',{'form' :form})





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
    tags_with_images = []
    for tag_ in all_tags:
        if Images.objects.filter(tags__tag__icontains=tag_).count()>0:
            tags_with_images.append(tag_)

    return render(request,
        'photohireapp/search.html',
        {
            'tagged_images': tagged_images,
            'tag':tag,
            'all_tags': tags_with_images
        }
    )

def user_profile(request, user_id):
    user_data = Profile.objects.get(id=user_id)
    rating_obj = Ratings.objects.filter(user_id=user_id)
    ratings = [r.rating for r in rating_obj]

    if len(ratings):
        avg_rating = sum(ratings)/len(ratings)
    else:
        avg_rating = -1

    # Any number between 5 and 15
    n_recommended = random.randint(5,15)

    # randomly pick 'n_recommended' images from the database
    recommended_images = Images.objects.order_by('?')[:n_recommended]
    return render(request, 'photohireapp/profile.html', 
        {'user_data':user_data,
        'recommended_images':recommended_images,
        'n_recommended':n_recommended,
        'avg_rating':avg_rating,
        'user_id':user_id
        }
    )


def like_image(request, img_id):
    img_data = Images.objects.get(id=img_id)
    img_data.likes = img_data.likes + 1
    img_data.save()
    return redirect(request.META['HTTP_REFERER'])
from django.http import HttpResponse
from django.shortcuts import render, redirect,reverse
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from .forms import *
from .models import *
import random

def logout_view(request):
    logout(request)
    return redirect('signin')

def user_profile(request):
        if request.method=='POST':
            form= editprofileform(request.POST, instance=request.user)
            if form.is_valid():
                bio=form.cleaned_data['bio']
                user=User.objects.get(id=request.user.id).id
                update=Profile.objects.filter(user=user).update(bio=bio)
            else:
                print(form.errors)
        else:
            form=editprofileform(instance=request.user)

        return render(request,'photohireapp/edit_profile.html',{'form':form})
	
def home(request):
    images = list(Images.objects.all().order_by('-likes'))

    # Get top 5 photographers based on Profile views
    photographers = list(Profile.objects.filter(is_photographer=True).order_by('-profile_views')[:5])

    # Shuffle lists
    random.shuffle(photographers)

    # Get first 3 from the shuffled list of 5 photographers
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
    
    list_of_pg = []
    
    for pg in trending_photographers:
        rating_obj = Ratings.objects.filter(user_id=pg.id)
        ratings = [r.rating for r in rating_obj]

        if len(ratings):
            avg_rating = round(sum(ratings)/len(ratings),1)
        else:
            avg_rating = -1

        pg.rating = avg_rating
        list_of_pg.append(pg)

    return render(request, 
        'photohireapp/expore.html',
        {'images':images, 'list_of_pg':list_of_pg}
    )


@csrf_exempt
def signup(request):
    if request.method=='POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user =form.save()
            user.refresh_from_db()
            user.profile.first_name=form.cleaned_data.get('first_name')
            user.profile.last_name=form.cleaned_data.get('last_name')
            user.profile.is_photographer=form.cleaned_data.get('is_photographer')

            # Set email = username
            user.email = user.username
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
        else:
            print(form.errors)
        return redirect('/')
    else:
        form=UserCreationForm()
        args={'form':form}
        return render(request,"photohireapp/sign-up.html",args)
    return render(request, 
        'photohireapp/sign-in.html'
    )


@csrf_exempt
def signin(request):
    if request.method =='POST':
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

def user_profile(request, user_id, image_id=-1):
    user_data = Profile.objects.get(id=user_id)

    user_data.profile_views = user_data.profile_views + 1
    user_data.save()

    ## Get social_data if it exists
    try:
        social_data = Social.objects.get(user_id=user_id)
    except Exception:
        social_data = {}

    rating_obj = Ratings.objects.filter(user_id=user_id)
    ratings = [r.rating for r in rating_obj]
    if len(ratings):
        # Round off to only one digit to have ratings like 4.3 and not 4.333333333
        avg_rating = round(sum(ratings)/len(ratings), 1)
    else:
        avg_rating = -1
    
    bookings = Bookings.objects.filter(photographer_id=user_id)

    # Any number between 5 and 15
    n_recommended = random.randint(5,15)
    # randomly pick 'n_recommended' images from the database
    recommended_images = Images.objects.order_by('?')[:n_recommended]
    ## Reviews and ratings
    if request.method=="POST":
        rating_form = RatingsForm(request.POST)
        rating_form.save()
    else:
        rating_form = RatingsForm()

    # Photos uploaded by current photographer
    uploaded_images = Images.objects.filter(user_id=user_id)

    context = {'user_data':user_data,
        'recommended_images':recommended_images,
        'uploaded_images': uploaded_images,
        'avg_rating':avg_rating,
        'rating_form': rating_form,
        'rating_obj':rating_obj,
        'social_data': social_data,
        'bookings': bookings
        }

    # If the call is from delete_image() return context only
    if image_id != -1:
        return context

    return render(request, 'photohireapp/profile.html', context)


def like_image(request, img_id):
    img_data = Images.objects.get(id=img_id)
    img_data.likes = img_data.likes + 1
    img_data.save()
    return redirect(request.META['HTTP_REFERER'])


def upload_images(request, user_id): 

	if request.method == 'POST': 
		form = ImagesForm(request.POST, request.FILES) 

		if form.is_valid(): 
			form.save()
			messages.add_message(request, messages.INFO, "Image Uploaded successfully!")
			
			# Redirect to the same page
			return redirect(request.META['HTTP_REFERER'])
	else: 
		form = ImagesForm() 
	return render(request, 'photohireapp/upload_images.html', {'form' : form})


def delete_image(request, user_id, image_id):
    instance = Images.objects.get(id=image_id)
    instance.delete()
    
    # Add message
    messages.add_message(request, messages.INFO, "Image deleted successfully")

    return redirect('/user_profile/'+str(user_id))


@csrf_exempt
def edit_profile(request, user_id):
    user_data = Profile.objects.get(id=user_id)
    try:
        social_data = Social.objects.get(user_id=user_id)
    except Exception as e:
        print(e)
        social_data = {}

    if request.method == "POST":
        pofile_form = ProfileForm(request.POST or None, request.FILES or None,  instance=user_data)

        # If social data not retrieved, get a creat form else get an update form
        if social_data == {}:
            social_form = SocialForm(request.POST)
        else:
            social_form = SocialForm(request.POST, instance=social_data)

        # If both forms valid, proceed forward
        if pofile_form.is_valid() and social_form.is_valid():
            profile_edit = pofile_form.save(commit=False)
            profile_edit.save()
            social_edit = social_form.save(commit=False)
            social_edit.save()
            return redirect('/user_profile/'+str(user_id))
        else:
            print(pofile_form.errors, social_form.errors)
    return render(request, 'photohireapp/edit_profile.html', {'user_data':user_data, 'social_data':social_data})

@csrf_exempt
def hire(request, pg_id):
    hire_form = BookingsForm()
    if request.method == "POST":
        hire_form = BookingsForm(request.POST)
        print(request.POST)
        if hire_form.is_valid():
            hire_form.save()
        else:
            print(hire_form.errors)
    return render(request, 'photohireapp/hire.html', {'hire_form':hire_form, 'pg_id':pg_id})

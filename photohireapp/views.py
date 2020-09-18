from django.http import HttpResponse
from django.shortcuts import render, redirect,reverse
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from django.core.mail import send_mail
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
    # Get all images by number of likes
    # Minus (-liked) if for descending order
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


# csrf_exempt is for all the form related views in django
@csrf_exempt
def signup(request):
    # POST request when clicked on submit
    if request.method=='POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user =form.save()
            user.refresh_from_db()
            user.profile.first_name=form.cleaned_data.get('first_name')
            user.profile.last_name=form.cleaned_data.get('last_name')

            # Set is_photographer to True or False based on the radio button pressed
            user.profile.is_photographer = True if request.POST['is_photographer'] == "photographer" else False

            # Set email = username
            user.email = user.username
            user.save()
            raw_password = form.cleaned_data.get('password1')

            # make the user login automatically after sign-up
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            # Add success message
            messages.add_message(request, messages.INFO, "Congrats! You signed up successfully!")

            return redirect('/')
        else:
            messages.add_message(request, messages.INFO, str(form.errors))
            print(form.errors)
            return redirect('/sign-up')
    else:
        form=UserCreationForm()
        args={'form':form}
        return render(request,"photohireapp/sign-up.html",args)
    return render(request, 
        'photohireapp/sign-in.html'
    )


@csrf_exempt
def signin(request):

    # When user clicked Submit
    if request.method =='POST':

        # Get all data from request.POST
        form=LoginForm(request.POST)

        if form.is_valid():
            cd =form.cleaned_data

            # Check if user is correct
            user=authenticate(username = cd['email'] , password = cd['password'])

            # If user is there, make him login
            if user:
                login(request,user)
                return redirect('/user_profile/'+str(user.id))
            
            # Give him an error of 404
            else:
                messages.add_message(request, messages.INFO, "User does not exist!")
        
        # If the form if invalid, just print errors
        else:
            print(form.errors)
            messages.add_message(request, messages.INFO, str(form.errors))

    # When user came on login page
    else:
        form=LoginForm()
    return render(request , 'photohireapp/sign-in.html',{'form' :form})


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

    # Get all tags, that have atleast one image for them
    tags_with_images = []

    # Iterate for all tags
    for tag_ in all_tags:

        # If image exists for that tag
        if Images.objects.filter(tags__tag__icontains=tag_).count()>0:

            # Add that tag to the tags_with_images
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

    # Get all data for that user
    user_data = Profile.objects.get(id=user_id)

    # Increase his views by 1
    user_data.profile_views = user_data.profile_views + 1
    user_data.save()

    ## Get social_data if it exists
    try:
        social_data = Social.objects.get(user_id=user_id)
    except Exception:
        social_data = {}
    
    ## Calculate average rating
    rating_obj = Ratings.objects.filter(user_id=user_id)
    ratings = [r.rating for r in rating_obj]

    if len(ratings) > 0:
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

    return render(request, 'photohireapp/profile.html', context)


def like_image(request, img_id):
    img_data = Images.objects.get(id=img_id)
    img_data.likes = img_data.likes + 1
    img_data.save()

    # Return to the same page
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
			messages.add_message(request, messages.INFO, str(form.errors))
	else: 
		form = ImagesForm() 
	return render(request, 'photohireapp/upload_images.html', {'form' : form, 'user_id':user_id})


def delete_image(request, image_id):
    instance = Images.objects.get(id=image_id)
    instance.delete()
    
    # Add message
    messages.add_message(request, messages.INFO, "Image deleted successfully")

    # Redirect to the same page again
    return redirect(request.META['HTTP_REFERER'])


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


def send_hiring_emails(request_values):
    print(request_values)

    # Get necessary values first
    event = request_values['event']
    booking_from = request_values['booking_from']
    booking_to = request_values['booking_to']
    customer_name = Profile.objects.get(id=request_values['user_id'])
    photographer_name = Profile.objects.get(id=request_values['photographer_id'])

    customer_email = User.objects.get(id=request_values['user_id']).email
    photographer_email = User.objects.get(id=request_values['photographer_id']).email


    # Send email to the Customer
    send_mail(
        'Congratulations! You hired - ' + str(photographer_name),
        'Hi, \n\nThank you for using our service. You hired the photographer named "' + str(photographer_name) + '".\nBelow are the details. \n\nEVENT: "' + event + '"\nFROM DATE: ' + booking_from + ' \nTO DATE: ' + booking_to + '\n\nWe hope you enjoy our service. \n\nKind regards, \nTeam FindYourLensman',
        'app.find.your.lensman@gmail.com',
        [customer_email],
        fail_silently=False,
    )

    # Send email to the Photographer
    send_mail(
        'Congratulations! You got hired by - ' + str(customer_name),
        'Hi, \n\nYou got hired by a customer named "' + str(customer_name) + '".\nBelow are the details. \n\nEVENT: "' + event + '"\nFROM DATE: ' + booking_from + '\nTO DATE: ' + booking_to + '\n\nBe ready to click some awesome photos. Good Luck! \n\nKind regards, \nTeam FindYourLensman',
        'app.find.your.lensman@gmail.com',
        [photographer_email],
        fail_silently=False,
    )

@csrf_exempt
def hire(request, pg_id):
    hire_form = BookingsForm()
    if request.method == "POST":
        hire_form = BookingsForm(request.POST)
        if hire_form.is_valid():
            hire_form.save()
            messages.add_message(request, messages.INFO, "You hired this photographer sucessfully! Please check your email for more details!")

            # Just send eveything to the funtion and it will send two emails!
            send_hiring_emails(request.POST)
        else:
            print(form.errors)
            messages.add_message(request, messages.ERROR, str(form.errors))
    return render(request, 'photohireapp/hire.html', {'hire_form':hire_form, 'pg_id':pg_id})

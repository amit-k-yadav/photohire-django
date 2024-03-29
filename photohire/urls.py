from django.contrib import admin 
from django.urls import path,include 
from django.conf import settings 
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# Import all the views from 'views.py'
from photohireapp.views import *

app_name='photohireapp'

urlpatterns = [
    path('', home, name = 'home'),
    path('admin/', admin.site.urls),        # Django default URL
    path('explore/', explore, name='explore'),
    path('sign-in/', signin, name='signin'),
    path('sign-up/', signup, name='signup'),
    path('about/', about, name='about'),
    path('search/', search, name='search'),

    # Takes to a user profile with specific ID
    path('user_profile/<int:user_id>', user_profile, name="user_profile"),
	path('logout_view/', logout_view, name='logout_view'),

    # Likes an image with specific ID
    path('like/<int:img_id>', like_image, name='like_image'),
    path('upload_images/<int:user_id>', upload_images, name = 'upload_images'),

    # Deletes a photo with id=image_id
    path('delete_image/<int:image_id>', delete_image, name = 'delete_image'),
    path('edit_profile/<int:user_id>', edit_profile, name = 'edit_profile'),

    # Hire a photographer with id=pg_id
    path('hire/<int:pg_id>', hire, name="hire"),


    ############## Start : Password reset URLs ##############

    # Forget Password - Renders "password_reset_form.html"
    # "auth_views.PasswordResetView.as_view" view below is a library and it's executed by django
    path('password-reset/',
        auth_views.PasswordResetView.as_view(
             template_name='registrations/password_reset_form.html',
             subject_template_name='registrations/password_reset_subject.txt',
             email_template_name='registrations/password_reset_email.html'
         ),
         name='password_reset'),


    # User get redirected here after entering his/her email - Renders "password_reset_form.html"
    # "auth_views.PasswordResetDoneView.as_view" view below is a library and it's executed by django
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registrations/password_reset_done.html'
         ),
         name='password_reset_done'),


    # User comes here when he/she clicks the link in the email - Renders "password_reset_confirm.html"
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registrations/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),


    # This is for information after user has changed the password
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registrations/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    
    ############## END : Password reset URLs ##############
]

# This is additional URL used for Static content (i.e CSS and JavaScript etc.)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# This is additional URL used for Media content (i.e images, profile pictures etc.)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

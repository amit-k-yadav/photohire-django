from django.contrib import admin 
from django.urls import path,include 
from django.conf import settings 
from django.conf.urls.static import static 
from photohireapp.views import *
app_name='photohireapp' 
urlpatterns = [ 
    path('', home, name = 'home'),
    path('admin/', admin.site.urls),
    path('explore/', explore, name='explore'),
    path('sign-in/', signin, name='signin'),
    path('sign-up/', signup, name='signup'),
    path('about/', about, name='about'),
    path('search/', search, name='search'),
    path('user_profile/<int:user_id>', user_profile, name="user_profile"),
    path('login/', signin, name="signin"),
	path('user_profile/', user_profile, name='user_profile'),
	path('logout_view/', logout_view, name='logout_view'),
    path('like/<int:img_id>', like_image, name='like_image'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

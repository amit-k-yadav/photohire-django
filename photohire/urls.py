from django.contrib import admin 
from django.urls import path,include 
from django.conf import settings 
from django.conf.urls.static import static 
from photohireapp.views import *
  
urlpatterns = [ 
    path('', home, name = 'home'),
    path('admin/', admin.site.urls),
    path('profile/', include('photohireapp.urls')),
    path('explore/', explore, name='explore'),
    path('sign-in/', signin, name='signin'),
    path('sign-up/', signup, name='signup'),
    path('about/', about, name='about'),
    path('search/', search, name='search'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

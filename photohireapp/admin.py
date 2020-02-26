from django.contrib import admin
from .models import *

admin.site.register(Person)
admin.site.register(Tags)
admin.site.register(Images)
admin.site.register(Like)
admin.site.register(Bookings)
admin.site.register(Social)
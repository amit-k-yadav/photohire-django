from django.contrib import admin
from .models import *

admin.site.register(Bookings)
admin.site.register(Social)

class TagsAdmin(admin.ModelAdmin):
    list_display = ('tag',)
    list_filter = ('tag',)
admin.site.register(Tags, TagsAdmin)

class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'email',
        'address',
        'bio',
        'is_photographer',
        'profile_picture'
        )
admin.site.register(Person, PersonAdmin)

class ImagesAdmin(admin.ModelAdmin):
    list_display = (
        'image',
        'user_id',
        'tags',
        'likes',
        'upload_timestamp'
        )
admin.site.register(Images, ImagesAdmin)
from django.contrib import admin
from .models import *

class BookingsAdmin(admin.ModelAdmin):
    list_display = ('user_id','photographer_id','event', 'booking_from', 'booking_to', 'booking_timestamp')
admin.site.register(Bookings, BookingsAdmin)

class SocialAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'twitter_handle',
        'instagram_id',
        'pinterest_id',
        'youtube_channel',
    )
admin.site.register(Social, SocialAdmin)

class TagsAdmin(admin.ModelAdmin):
    list_display = ('tag',)
    list_filter = ('tag',)
admin.site.register(Tags, TagsAdmin)

class ProfileAdmin(admin.ModelAdmin):
   list_display = (
       'first_name',
       'last_name',
       'bio',
       'is_photographer',
       'profile_picture',
       'profile_views'
       )
admin.site.register(Profile, ProfileAdmin)

class ImagesAdmin(admin.ModelAdmin):
    list_display = (
        'image',
        'user_id',
        'tags',
        'likes',
        'upload_timestamp'
        )
admin.site.register(Images, ImagesAdmin)

class RatingsAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'rating',
        'review'
    )
admin.site.register(Ratings, RatingsAdmin)
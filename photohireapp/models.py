from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save

from django.dispatch import receiver

class Profile(models.Model):
    first_name = models.CharField(max_length=200,default='first')
    last_name = models.CharField(max_length=200,default='second')
    #email = models.EmailField(max_length=254)
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default=1)	
    #address = models.TextField(blank=True)
    bio = models.TextField(blank=True,null=True)
    is_photographer = models.BooleanField(default=False)
    profile_views = models.IntegerField(default=0)
    profile_picture = models.ImageField(upload_to='images/',blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)







@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class Tags(models.Model):
    tag = models.CharField(max_length=200)
    def __str__(self):
        return self.tag

    class Meta:
        ordering = ['tag']


class Images(models.Model):
    image = models.ImageField(upload_to='images/')
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ForeignKey(Tags, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(default=0)
    upload_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.image)

    class Meta:
        ordering = ['upload_timestamp']


class Bookings(models.Model):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='customer_id')
    photographer_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='photographer_id')
    event = models.CharField(max_length=300)
    event_date = models.DateField(auto_now=False)
    booking_from = models.DateField(auto_now=False)
    booking_to = models.DateField(auto_now=False)
    booking_timestamp = models.DateTimeField(auto_now=True)

class Social(models.Model):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    twitter_handle = models.CharField(max_length=200, blank=True)
    instagram_id = models.CharField(max_length=200, blank=True)
    pinterest_id = models.CharField(max_length=200, blank=True)
    youtube_channel = models.CharField(max_length=200, blank=True)

class Ratings(models.Model):
    rating = models.IntegerField(choices=[(i, i) for i in range(0, 6)], blank=True)
    review = models.CharField(blank=True, max_length=200)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)

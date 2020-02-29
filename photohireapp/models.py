from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    address = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    is_photographer = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='images/',blank=True)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Tags(models.Model):
    tag = models.CharField(max_length=200)
    def __str__(self):
        return self.tag

    class Meta:
        ordering = ['tag']


class Images(models.Model):
    image = models.ImageField(upload_to='images/')
    user_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    tags = models.ForeignKey(Tags, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(default=0)
    upload_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.image)

    class Meta:
        ordering = ['upload_timestamp']


class Bookings(models.Model):
    user_id = models.ForeignKey(Person, on_delete=models.CASCADE,related_name='customer_id')
    photographer_id = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='photographer_id')
    event = models.CharField(max_length=300)
    event_date = models.DateField(auto_now=False)
    booking_from = models.DateField(auto_now=False)
    booking_to = models.DateField(auto_now=False)
    booking_timestamp = models.DateTimeField(auto_now=True)

class Social(models.Model):
    user_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    twitter_handle = models.CharField(max_length=200, blank=True)
    instagram_id = models.CharField(max_length=200, blank=True)
    pinterest_id = models.CharField(max_length=200, blank=True)
    youtube_channel = models.CharField(max_length=200, blank=True)

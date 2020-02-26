from django.db import models


class Hotel(models.Model): 
    name = models.CharField(max_length=50) 
    hotel_Main_Img = models.ImageField(upload_to='images/')


class Users(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    address = models.TextField()
    bio = models.TextField()
    is_photographer = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='images/')

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Tags(models.Model):
    tag = models.CharField(max_length=200)
    def __str__(self):
        return self.tag

    class Meta:
        ordering = ['tag']


class Images(models.Model):
    url = models.URLField(max_length=5000)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    tags = models.ForeignKey(Tags, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField()
    upload_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.upload_timestamp

    class Meta:
        ordering = ['upload_timestamp']


class Like(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    image_id = models.ForeignKey(Images, on_delete=models.CASCADE)
    liked_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.liked_timestamp

    class Meta:
        ordering = ['liked_timestamp']


class Bookings(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE,related_name='customer_id')
    photographer_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='photographer_id')
    event = models.CharField(max_length=300)
    event_date = models.DateField(auto_now=False)
    booking_from = models.DateField(auto_now=False)
    booking_to = models.DateField(auto_now=False)
    booking_timestamp = models.DateTimeField(auto_now=True)

class Social(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    twitter_handle = models.CharField(max_length=200)
    instagram_id = models.CharField(max_length=200)
    pinterest_id = models.CharField(max_length=200)
    youtube_channel = models.CharField(max_length=200)
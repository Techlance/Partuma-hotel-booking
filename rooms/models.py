from django.db import models

# Create your models here.


# Model for Rooms (can be accessed by admin only)
class Rooms(models.Model):
    room_type = models.TextField(max_length=1000, default="")
    no_of_rooms = models.IntegerField(default=0)
    room_price = models.IntegerField(default=0) # Rate per day
    rate_for_extra_bed = models.IntegerField(default=0.0) # Rate per day
    taxes = models.IntegerField(default=0)
    max_persons = models.IntegerField(default=0)
    discription = models.TextField(max_length=10000, default="")
    room_size = models.IntegerField(default=0)
    wifi = models.BooleanField(default=False)
    gym = models.BooleanField(default=False)
    tv = models.BooleanField(default=False)
    breakfast = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    dinner = models.BooleanField(default=False)
    swimming_pool = models.BooleanField(default=False)
    air_conditioning = models.BooleanField(default=False)
    room_photo = models.ImageField(upload_to="rooms_image/", default="media/about3.jpg")

    def __str__(self):
        return self.room_type


# Models for user who booked room
class Booked(models.Model):
    name = models.TextField(max_length=100)
    phone_number = models.TextField(max_length=15)
    e_mail = models.TextField()
    no_of_rooms = models.IntegerField()
    no_of_adults = models.IntegerField()
    no_of_children = models.IntegerField()
    total_price = models.IntegerField()
    check_in = models.DateField()
    check_out = models.DateField()
    room_type = models.ForeignKey(to=Rooms, on_delete=models.CASCADE)

    def __str__(self):
        return self.name






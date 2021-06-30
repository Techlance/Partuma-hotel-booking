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
    room_photo_1 = models.ImageField(upload_to="rooms_image/", default="media/about3.jpg")
    room_photo_2 = models.ImageField(upload_to="rooms_image/", default="media/about3.jpg")
    room_photo_3 = models.ImageField(upload_to="rooms_image/", default="media/about3.jpg")
    room_photo_4 = models.ImageField(upload_to="rooms_image/", default="media/about3.jpg")
    room_photo_5 = models.ImageField(upload_to="rooms_image/", default="media/about3.jpg")

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

class Contact(models.Model):
    name = models.TextField(max_length=100)
    e_mail = models.TextField()
    subject = models.TextField()
    message = models.TextField()
    def __str__(self):
        return self.name





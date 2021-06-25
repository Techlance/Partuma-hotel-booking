from django.db import models

# Create your models here.

class Rooms(models.Model):
    room_type = models.TextField()
    no_of_rooms = models.IntegerField()

    def __str__(self):
        return self.room_type

class Booked(models.Model):
    name = models.TextField()
    phone_number = models.TextField()
    address = models.TextField()
    government_id = models.TextField()
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






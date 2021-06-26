from django.contrib import admin
from .models import Rooms, Booked, Contact
# Register your models here.

admin.site.register(Rooms)
admin.site.register(Booked)
admin.site.register(Contact)

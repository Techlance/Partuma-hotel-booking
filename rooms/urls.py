from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name="home_page"),
    path('check_availability', views.check_availability, name="check_availability"),
    path('booking', views.Booking_Page, name="booking")
]
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name="home_page"),
    # path('check_availability', views.check_availability, name="check_availability"),
    path('booking', views.Booking_Page, name="booking"),
    path('rooms', views.all_rooms, name="all_rooms"),
    path('contact', views.contact, name="contact"),
    path('rooms/<int:id>', views.single_room, name="single_room"),
    path('about', views.about, name="about"),
    path('ajax/send_data', views.send_user_data, name="send_data"),
    path('single_booking', views.Booking_Single_Page, name="single_booking")
] 
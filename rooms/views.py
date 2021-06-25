from django.shortcuts import redirect, render
from .models import Booked, Rooms
# Create your views here.


def home_page(request):
    return render(request, "index.html")

def check_availability(request):
    if request.method=="GET":
        return render(request, "check_availability.html")
    else:
        checkin = request.POST.get('check_in')
        checkout = request.POST.get('check_out')
        print(checkin, checkout)
        return redirect('check_availability')

def Booking_Page(request):
    if request.method=="GET":
        return render(request, "booking_form.html")
    else:
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        government_id = request.POST.get('government_id')
        email = request.POST.get('email')
        no_of_rooms = request.POST.get('no_of_rooms')
        no_of_adults = request.POST.get('no_of_adults')
        no_of_childern = request.POST.get('no_of_children')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        type_of_room = Rooms.objects.get(id=1)
        new_booking = Booked()
        new_booking.name = name
        new_booking.phone_number = phone_number
        new_booking.address = address
        new_booking.government_id = government_id
        new_booking.e_mail = email
        new_booking.no_of_rooms = no_of_rooms
        new_booking.no_of_adults = no_of_adults
        new_booking.no_of_children = no_of_childern
        new_booking.check_in =  check_in
        new_booking.check_out = check_out
        new_booking.room_type = type_of_room
        new_booking.total_price = 0
        new_booking.save()
        return redirect('booking')



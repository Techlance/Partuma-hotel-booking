from django.shortcuts import redirect, render
from .models import Booked, Rooms
from datetime import *
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
        
        request_checkin = date(int(checkin[:4]), int(checkin[5:7]), int(checkin[8:]))
        request_checkout = date(int(checkout[:4]), int(checkout[5:7]), int(checkout[8:]))
        all_booked = Booked.objects.all()
        room1 = 0
        room2 = 0
        for i in all_booked:
            full_date = i.check_in
            full_date_1 = i.check_out
            # temp1 = str(temp.year)
            # print(temp1)
            # print(type(temp1))
            fetched_checkin = date(int(full_date.year), int(str(full_date.month)), int(str(full_date.day)))
            fetched_checkout = date(int(full_date_1.year), int(str(full_date_1.month)), int(str(full_date_1.day)))
            print(request_checkin, fetched_checkin, request_checkout, fetched_checkout)
            if (request_checkin < fetched_checkin and request_checkout <= fetched_checkin) or (request_checkin >= fetched_checkout and request_checkout > fetched_checkout):
                pass
            else:
                print(i.room_type_id)
                if i.room_type_id==1:
                    room1 += 1
                else:
                    room2 += 1
        print(room1)
        print(room2)
        all_rooms = Rooms.objects.all()
        j = 0
        for i in all_rooms:
            if j==0:
                print("Available rooms-2", i.room_type, i.no_of_rooms-room2)
            else:
                print("Available rooms-1", i.room_type, i.no_of_rooms-room1)
            j += 1

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



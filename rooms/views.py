from django.shortcuts import redirect, render
from .models import Booked, Rooms
from datetime import *
# Create your views here.

# end-route : ''
def home_page(request):
    return render(request, "index.html")

# end-route : check_availability
def check_availability(request):
    if request.method=="GET":
        return render(request, "check_availability.html")
    else:
        # Get Data from user
        checkin = request.POST.get('check_in')
        checkout = request.POST.get('check_out')
        print(checkin, checkout)
        
        # parse date data to compare with dates fetched from database
        # request_checkin = check-in Date obtained from user using POST request
        # request_checkout = check-out Date obtained from user using POST request
        request_checkin = date(int(checkin[:4]), int(checkin[5:7]), int(checkin[8:]))
        request_checkout = date(int(checkout[:4]), int(checkout[5:7]), int(checkout[8:]))

        # Query to get all user who booked rooms
        all_booked = Booked.objects.all()

        #

        dict = {}
        all_rooms = Rooms.objects.all()
        for i in all_rooms:
            dict.update({i.id : 0})
        print(dict)

        # Logic for checking How many room is available between user's demanded date
        for i in all_booked:
            full_date_ci = i.check_in  # ci = check in
            full_date_co = i.check_out # co = check out
            fetched_checkin = date(int(full_date_ci.year), int(str(full_date_ci.month)), int(str(full_date_ci.day)))
            fetched_checkout = date(int(full_date_co.year), int(str(full_date_co.month)), int(str(full_date_co.day)))
            print(request_checkin, fetched_checkin, request_checkout, fetched_checkout)
            if (request_checkin < fetched_checkin and request_checkout <= fetched_checkin) or (request_checkin >= fetched_checkout and request_checkout > fetched_checkout):
                pass
            else:
                dict[i.room_type_id] += i.no_of_rooms
        
        rem_rooms = {} # Dictionary to store remaining rooms of each type 
        for i in all_rooms:
            rem_rooms.update({i.id:i.no_of_rooms - dict[i.id]})
        print(rem_rooms)
        return redirect('check_availability')

# end route : booking
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
        new_booking.total_price = 0 # calculation is remaining 
        new_booking.save()
        return redirect('booking')



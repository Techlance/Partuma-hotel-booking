from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Booked, Rooms, Contact
from datetime import *

# Create your views here.


# Reusable function to check available dates
def check_availability(input_date):
    if len(input_date)==0:
            return False
    checkin = input_date[:10]
    checkout = input_date[13:]
    
    # parse date data to compare with dates fetched from database
    # request_checkin = check-in Date obtained from user using POST request
    # request_checkout = check-out Date obtained from user using POST request
    request_checkin = date(int(checkin[:4]), int(checkin[5:7]), int(checkin[8:]))
    request_checkout = date(int(checkout[:4]), int(checkout[5:7]), int(checkout[8:]))
    difference_days = request_checkout - request_checkin
    no_of_days_requested = difference_days.days
    # Query to get all user who booked rooms
    all_booked = Booked.objects.all()

    
    # This Dictionary contains rooms of each type
    dict = {}
    all_rooms = Rooms.objects.all()
    for i in all_rooms:
        dict.update({i.id : 0})
    

    # Logic for checking How many room is available between user's demanded date
    for i in all_booked:
        full_date_ci = i.check_in  # ci = check in
        full_date_co = i.check_out # co = check out
        fetched_checkin = date(int(full_date_ci.year), int(str(full_date_ci.month)), int(str(full_date_ci.day)))
        fetched_checkout = date(int(full_date_co.year), int(str(full_date_co.month)), int(str(full_date_co.day)))
       
        # request checkin/checkout means date send by client side
        # fetched checkin/checkout means booked dates fetched from database
        # compare request checkin and checkout with fetched checkin and checkout
        if (request_checkin < fetched_checkin and request_checkout <= fetched_checkin) or (request_checkin >= fetched_checkout and request_checkout > fetched_checkout):
            pass
        else:
            dict[i.room_type_id] += i.no_of_rooms
    
    rem_rooms = {} # Dictionary to store remaining rooms of each type 
    for i in all_rooms:
        if i.no_of_rooms - dict[i.id] >= 0:
            rem_rooms.update({i.id:i.no_of_rooms - dict[i.id]})
        else:
            rem_rooms.update({i.id:0})
    
    rooms = Rooms.objects.all()
    return {'rooms':rooms, 'rem_rooms':rem_rooms, 'no_of_days_requested':no_of_days_requested}


# end-route : ''
def home_page(request):
    if request.method=="GET":
        return render(request, "index.html")
    else:
        # Get Data from user
        input_date = request.POST.get('check_in')
        context = check_availability(input_date)
        if context==False:
            messages.warning("Please select a Date")
            return redirect('')
        else:
            return render(request, "room.html", context)


# end-route : rooms
def all_rooms(request):
    if request.method=="GET":
        rooms = Rooms.objects.all()
        return render(request, "room.html", {'rooms':rooms})


# end-route : rooms/<int:id>
def single_room(request, id):
    rooms= Rooms.objects.get(id=id)
    request.session['room_type'] = rooms.room_type
    request.session['room_type_id'] = id
    return render(request, "room-single.html", {'rooms':rooms})


# end route : booking
def Booking_Page(request):
    if request.method=="GET":
        rooms = Rooms.objects.all()
        return render(request, "booking.html", {'rooms':rooms})
    else:
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        input_date = request.POST.get('check_in')
        type_of_room = request.POST.get('room_type') 
        no_of_rooms = int(request.POST.get('no_of_rooms'))
        no_of_adults = int(request.POST.get('no_of_adults'))
        no_of_children = int(request.POST.get('no_of_children'))
        
        checkin = input_date[:10]
        checkout = input_date[13:]
        
        # parse date data to compare with dates fetched from database
        # request_checkin = check-in Date obtained from user using POST request
        # request_checkout = check-out Date obtained from user using POST request
        request_checkin = date(int(checkin[:4]), int(checkin[5:7]), int(checkin[8:]))
        request_checkout = date(int(checkout[:4]), int(checkout[5:7]), int(checkout[8:]))
        difference_days = request_checkout - request_checkin
        no_of_days_requested = difference_days.days
        
        
        room_data = Rooms.objects.get(id=type_of_room)
        total_price = int(room_data.room_price)*int(no_of_rooms)*int(no_of_days_requested)
        print(total_price)
        booking = Booked()
        booking.name = name
        booking.phone_number = phone_number
        booking.email = email
        booking.no_of_rooms = no_of_rooms
        booking.no_of_adults = no_of_adults
        booking.no_of_children = no_of_children
        booking.total_price = total_price
        booking.check_in = request_checkin
        booking.check_out = request_checkout
        booking.room_type = room_data
        booking.save()
        
        return redirect('verification')


#end route : single_booking
def Booking_Single_Page(request):
    if request.method=="GET":
        rooms = Rooms.objects.all()

        # Stores room_type and room_type_id in session storage and pass it to the Booking page if user is redirected from route : rooms/<int:id>
        room_type = request.session['room_type']
        room_type_id = request.session['room_type_id']
        return render(request, "booking.html", {'rooms':rooms, 'room_type':room_type, 'room_type_id': room_type_id})


# end route : ajax/send_data
def send_user_data(request):
    # This function take room type and no of rooms as POST request from frontend using AJAX
    # Backend will send total price and total person as JsonResponse to frontend
    type_of_room = request.POST.get('room_type')
    no_of_rooms = request.POST.get('no_of_rooms')
    input_date = request.POST.get('check_in')
    context = check_availability(input_date)
    no_of_rooms = int(no_of_rooms)
    type_of_room = int(type_of_room)
    room_data = Rooms.objects.get(id=type_of_room)
    total_person = (room_data.max_persons)*no_of_rooms
    
    no_of_rooms_available = context['rem_rooms'][type_of_room]
    no_of_days = context['no_of_days_requested']
    total_price = (room_data.room_price)*no_of_rooms*int(no_of_days)
    data = {
        'max_person':total_person,
        'price':total_price,
        'no_of_rooms_available':no_of_rooms_available
    }
    return JsonResponse(data)


# end route : contact
def contact(request):
    if request.method=="GET":
        return render(request, "contact.html")
    else:
        # Function to save contact details in database
        name = request.POST.get('name')
        e_mail = request.POST.get('email')
        subject = request.POST.get('sub')
        message = request.POST.get('msg')
        contactObj = Contact()
        contactObj.name=name
        contactObj.e_mail=e_mail
        contactObj.subject=subject
        contactObj.message=message
        contactObj.save()
        messages.success(request, 'Your message has been sent')
        return redirect('contact')

def verification(request):
    return render(request, "verification.html")

# end-route : about  
def about(request):
    return render(request, 'about.html')






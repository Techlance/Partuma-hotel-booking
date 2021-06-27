from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Booked, Rooms, Contact
from datetime import *

# Create your views here.

# end-route : ''
def home_page(request):
    if request.method=="GET":
        return render(request, "index.html")
    else:
        # Get Data from user
        input_date = request.POST.get('check_in')
        if len(input_date)==0:
            messages.warning(request, 'Please enter a date')
            return redirect('')
        print("date", date)
        checkin = input_date[:10]
        print(len(checkin))
        checkout = input_date[13:]
        print(len(checkout))
        print(checkin)
        print(checkout)
        
        # parse date data to compare with dates fetched from database
        # request_checkin = check-in Date obtained from user using POST request
        # request_checkout = check-out Date obtained from user using POST request
        request_checkin = date(int(checkin[:4]), int(checkin[5:7]), int(checkin[8:]))
        request_checkout = date(int(checkout[:4]), int(checkout[5:7]), int(checkout[8:]))

        # Query to get all user who booked rooms
        all_booked = Booked.objects.all()

        
        # This Dictionary contains rooms of each type
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
            if i.no_of_rooms - dict[i.id] >= 0:
                rem_rooms.update({i.id:i.no_of_rooms - dict[i.id]})
            else:
                rem_rooms.update({i.id:0})
        print(rem_rooms)
        rooms = Rooms.objects.all()
        return render(request, "room.html", context={'rooms':rooms, 'rem_rooms':rem_rooms})

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
        no_of_rooms = request.POST.get('no_of_rooms')
        return redirect('booking')

def Booking_Single_Page(request):
    if request.method=="GET":
        rooms = Rooms.objects.all()
        room_type = request.session['room_type']
        room_type_id = request.session['room_type_id']
        request.session.flush()
        return render(request, "booking.html", {'rooms':rooms, 'room_type':room_type, 'room_type_id': room_type_id})



def send_user_data(request):
    type_of_room = request.POST.get('room_type')
    no_of_rooms = request.POST.get('no_of_rooms')
    no_of_rooms = int(no_of_rooms)
    type_of_room = int(type_of_room)
    room_data = Rooms.objects.get(id=type_of_room)
    total_person = (room_data.max_persons)*no_of_rooms
    total_price = (room_data.room_price)*no_of_rooms
    data = {
        'max_person':total_person,
        'price':total_price
    }
    return JsonResponse(data)





def contact(request):
    if request.method=="GET":
        return render(request, "contact.html")
    else:
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

# end-route : about  
def about(request):
    return render(request, 'about.html')






"""Developed by techlance 
   Date : 24-06-2021 to 30-06-2021"""




from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Booked, Rooms, Contact
from datetime import *
from datetime import datetime, timedelta
import time
import random
from django.conf import settings
from django.core.mail import send_mail
from twilio.rest import Client
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from io import BytesIO
from django.http import HttpResponse, request
import os
from django.template import Template, Context
from django.http import HttpResponse 
from django.template.loader import render_to_string
from django.shortcuts import HttpResponse
from django.template.loader import get_template, render_to_string
from fpdf import FPDF, HTMLMixin
# Create your views here.

# send sms to user
def send_sms(otp, to_):

    # Your Account SID from twilio.com/console
   
    account_sid = "ACb92105d6cb505863a13e05bef39dc8bd"
    # Your Auth Token from twilio.com/console
    auth_token  = "44705a3ce65f65f5c7bffc47e398311e"
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
        to=str(to_), 
        from_="+12512903658",
        body="Your otp is " + str(otp)  + " only valid for 05 mins ")


def partuma_confirmation(name, mob, room_type, no_of_rooms, checkin_date, checkout_date, price):
    # Your Account SID from twilio.com/console
   
    account_sid = "ACb92105d6cb505863a13e05bef39dc8bd"
    # Your Auth Token from twilio.com/console
   
    auth_token  = "44705a3ce65f65f5c7bffc47e398311e"

    client = Client(account_sid, auth_token)
    # print(to_)
    message = client.messages.create(
        to="+91" + str(9099038440), 
        from_="+12512903658",
        body = "Name : " + name + "\nMob : " + mob + "\nRoom Type : " + str(room_type) + "\nNo Of Rooms: " + str(no_of_rooms) + "\nCheckIn Date : " + checkin_date + "\ncheckOut Date : " + checkout_date + "\nPrice : " + str(price) + "\nhas booked a room from your site.")

    

# Above function will send text message to customer for their booking
def client_confirmation(name, mob, room_type, no_of_rooms, checkin_date, checkout_date, price):
    
    # Your Account SID from twilio.com/console
    account_sid = "ACb92105d6cb505863a13e05bef39dc8bd"
    # Your Auth Token from twilio.com/console
    auth_token  = "44705a3ce65f65f5c7bffc47e398311e"

    client = Client(account_sid, auth_token)
    # print(mob)
    message = client.messages.create(
        to= str(mob), 
        from_="+12512903658",
        body="Name : " + name + "\nMob : " + mob + "\nRoom Type : " + str(room_type) + "\nNo Of Rooms: " + str(no_of_rooms) + "\nCheckIn Date : " + checkin_date + "\ncheckOut Date : " + checkout_date + "\nPrice : " + str(price) + "\nyour provisional booking has been confrimed.")


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

# end route : booking
def Booking_Page(request):
    if request.method=="GET":
        rooms = Rooms.objects.all()
        return render(request, "booking.html", {'rooms':rooms})
    else:
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        # print(phone_number)
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

        context = check_availability(input_date)
        no_of_rooms_available = context['rem_rooms'][int(type_of_room)]
        if no_of_rooms_available >= no_of_rooms:
        
            # Generate OTP
            otp = random.randint(1000,9999)
            print("otp: ", otp)

            # User Data is stored in session till user is verified using OTP
            request.session['data'] = {'name': name, 'phone_number': phone_number, 'email': email ,'check_in': checkin, 'check_out':checkout, 'type_of_room': type_of_room, 'no_of_rooms': no_of_rooms, 'no_of_adults': no_of_adults,'no_of_children': no_of_children, 'no_of_days_requested':no_of_days_requested}
            request.session['otp']=otp
            expire_at = time.time() + 300   
            request.session['exp'] = expire_at
            try:
                # print(phone_number)
                send_sms(otp,phone_number)
                context = {
                        'var_phone': phone_number
                        }
                    
                return redirect("verification")
            except:
                request.session.flush()
                messages.warning(request, 'Please enter a valid phone number')
                response = redirect('booking')
                return response

            
        else:
            # if 2-3 three users clicks on book now for same type of room there will be problem so we handled that using above condition
            messages.info("Sorry.We Ran out of rooms!!")
            return redirect("booking")


# end route : verification 
# This function verfies OTP and redirect to checkout page if OTP is validated       
def verification(request):
    if request.session.get('otp', None):
        if request.method =='POST':
            if request.session.get('data', None):
                if time.time()>request.session['exp']:
                    context = {
                        'var_phone': request.session['data']['phone_number']
                    }
                    messages.warning(request, 'OTP was expired!')
                    response = redirect('verification')
                    return response
                elif(request.session['otp'] == int(request.POST.get('otp'))):
                    user_input = request.session['data']
                    room_data = Rooms.objects.get(id=user_input['type_of_room'])
                    total_price = int(room_data.room_price)*int(user_input['no_of_rooms'])*int(user_input['no_of_days_requested'])
                    user_data = Booked(name = user_input['name'],phone_number = user_input['phone_number'], e_mail = user_input['email'], no_of_rooms = user_input['no_of_rooms'],no_of_adults  = user_input['no_of_adults'], no_of_children  = user_input['no_of_children'],total_price=total_price , check_in =user_input['check_in'], check_out=user_input['check_out'], room_type=room_data)
                    user_data.save()
                    name  = user_input['name']
                    phone_number = user_input['phone_number']
                    email_1 = user_input['email']
                    check_in = user_input['check_in']
                    check_out = user_input['check_out']
                    no_of_rooms = user_input['no_of_rooms']
                    no_of_adults  = user_input['no_of_adults']
                    no_of_children  = user_input['no_of_children']
                    no_of_days = user_input['no_of_days_requested']
                    total_price=total_price
                    room_type=room_data.room_type
                    c = {
                        'var_phone': request.session['data']['phone_number'],
                        'name':name,
                        'phone_number':phone_number,
                        'email':email_1,
                        'check_in':check_in,
                        'check_out':check_out,
                        'no_of_rooms':no_of_rooms,
                        'no_of_adults':no_of_adults,
                        'no_of_children':no_of_children,
                        'room_type':room_data.room_type,
                        'total_price':total_price,
                        'no_of_days_requested':no_of_days,
                    }  
                    text_content = render_to_string('email.txt', c)
                    html_content = render_to_string('email.html', c)
                    try:
                        email = EmailMultiAlternatives('Partuma lodge and jazz club booking confirmed', text_content)
                        email.attach_alternative(html_content, "text/html")
                        email.to = [email_1]
                        email.send()
                        partuma_confirmation(user_input['name'], user_input['phone_number'], room_data.room_type, user_input['no_of_rooms'], user_input['check_in'], user_input['check_out'], str(total_price))
                        client_confirmation(user_input['name'], user_input['phone_number'], room_data.room_type, user_input['no_of_rooms'], user_input['check_in'], user_input['check_out'], str(total_price))
                        print("success")
                        response = redirect('checkout')
                        return response
                    except:
                        messages.warning(request, 'Please Enter valid email')
                        response = redirect('booking')
                        return response
                else:   
                    context = {
                    
                        'var_phone': request.session['data']['phone_number'],
                    
                    }
                    messages.warning(request, 'OTP was wrong!')
                    response = redirect('verification')
                    return response
                
            else:
                response = redirect('booking')
                return response
        else:
            user_input = request.session['data']
            room_data = Rooms.objects.get(id=user_input['type_of_room'])
            total_price = int(room_data.room_price)*int(user_input['no_of_rooms'])*int(user_input['no_of_days_requested'])
            context = {
                    
                'var_phone': request.session['data']['phone_number'],
                'user_input':user_input,
                'room_type':room_data.room_type,
                'total_price':total_price
            }
            response = render(request, 'verification.html', context)
            return response
    else:
        response = redirect('/')
        return response
       

# end route : resend_otp
# Above function resend OTP when user request for new OTP or if OTP expires
def resend_otp(request):
    if request.session.get('otp', None):
        # checks if OTP expired or not
        if time.time()>request.session['exp']:
            otp = random.randint(1000,9999)
            print("otp", otp)
            request.session['otp']=otp
            expire_at = time.time() + 300
            request.session['exp'] = expire_at

            send_sms(otp,request.session['data']['phone_number'])
            # send_sms(otp,mob)
            response = redirect('verification')
            return response
        else:
            response = redirect('verification')
            return response
    response = redirect('/')
    return response


# end-route : about  
def about(request):
    return render(request, 'about.html')


# end-route : checkout
def checkout(request):
    if request.session.get('data', None):
        user_input = request.session['data']
        room_data = Rooms.objects.get(id=user_input['type_of_room'])
        total_price = int(room_data.room_price)*int(user_input['no_of_rooms'])*int(user_input['no_of_days_requested'])
        context = {
            'user_input':user_input,
            'room_type':room_data.room_type,
            'total_price':total_price
        }
        try:
            del request.session['otp']
            del request.session['exp']
        except:
            pass
        
        return render(request, "checkout.html", context)
    else:
        return redirect("/")


class HtmlPdf(FPDF, HTMLMixin):
    pass


# end route : download_pdf
def GeneratePDF(request):

    # Function to download PDF provisional booking for Room booking
    user_input = request.session['data']
    room_data = Rooms.objects.get(id=user_input['type_of_room'])
    total_price = int(room_data.room_price)*int(user_input['no_of_rooms'])*int(user_input['no_of_days_requested'])
    name  = user_input['name']
    phone_number = user_input['phone_number']
    email_1 = user_input['email']
    check_in = user_input['check_in']
    check_out = user_input['check_out']
    no_of_rooms = user_input['no_of_rooms']
    no_of_adults  = user_input['no_of_adults']
    no_of_children  = user_input['no_of_children']
    no_of_days = user_input['no_of_days_requested']
    total_price=total_price
    room_type=room_data.room_type
    context = {
        'name':name,
        'phone_number':phone_number,
        'email':email_1,
        'check_in':check_in,
        'check_out':check_out,
        'no_of_rooms':no_of_rooms,
        'no_of_adults':no_of_adults,
        'no_of_children':no_of_children,
        'room_type':room_type,
        'total_price':total_price,
        'no_of_days_requested':no_of_days,
    }    
    pdf = HtmlPdf()
    pdf.add_page()
    pdf.write_html(render_to_string('pdf.html', context))
    response = HttpResponse(pdf.output(dest='S').encode('latin-1'))
    response['Content-Disposition'] = 'attachment; filename=' + "provisional_booking" + '.pdf'
    return response


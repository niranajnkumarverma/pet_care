from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.core.mail import send_mail
from random import randint
from django.conf import settings
from django.db.utils import *
from .symptoms import pet_symtops
from django.http import request

import os, re, time

user_image_path = os.path.join(settings.MEDIA_ROOT, 'image\\users\\')
# app_info
app_info = {
    'app_title': 'pet care house',
    'app_name': 'Pet Care',
    'msg_data': {'name': '', 'msg': '', 'type':'success', 'display': ''},
    'login': 'app/doctor_content.html'
}

def console(err):
    print(err)
    print('Type of error: ', type(err))
    print(err.args)

# set time out
def setTimeOut(method, start_from=0, delay=5):
    time_from = datetime.datetime.now()
    time_now = datetime.datetime.now()
    start_time = int( str( int(time_from.strftime('%H')) ) + str( int(time_from.strftime('%M')) ) )
    expire_time = int( str( int(time_now.strftime('%H')) ) + str( int(time_now.strftime('%M')) ) ) + delay
    if (expire_time-start_time) > delay:
        print('expired: ', expire_time-delay)
    print('date: ', expire_time-start_time)
    #return redirect(method)

# set time out 2
def timeOut(method, delay=1):
    start_time = datetime.datetime.now()
    app_info['time_out'] = {}
    app_info['time_out']['start_time'] = int( str( int(start_time.strftime('%H')) ) + str( int(start_time.strftime('%M')) ) )
    app_info['time_out']['out_point'] = delay
    app_info['time_out']['url'] = method
    
# check internet connection
def isConnected():
    try:
        url = request.get('http://google.com')
        status  = url.status_code
        if status:
            return True
    except Exception as err:
        app_info['msg_data']['name'] = 'Internet Not Available'
        app_info['msg_data']['msg'] = 'Check your internet connection.'
        return False

# default index/home page
def index(request):
    app_info['msg_data']['display'] = 'hide'
    if 'email' in request.session:
        profile_data(request)
        timeOut('logout')
        print('time: ', app_info['time_out'])
    return render(request, 'index.html', app_info)

# about page
def about_page(request):
    pass

# contact page
def contact_page(request):
    pass

####################################
## MAIN PAGES AND FUNCTIONALITIES ##
####################################

# send otp on mail
def send_otp(request, otp_for='reg'):
    app_info['verify_for'] = otp_for

    email_to_list = [request.session['email'],]
    subject = 'OTP for Forgot Password'
    otp = randint(1000,9999)
    print('OTP is: ', otp)
    request.session['otp'] = otp
    message = f"your one time otp for forgot password is: {otp}"
    email_from = settings.EMAIL_HOST_USER

    try:
        if isConnected():
            send_mail(subject, message, email_from, email_to_list)
        return True
    except settings.EMAIL_AUTH_ERROR as err:
        link = '((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)'
        get_link = re.findall(link, err.args[1].decode('utf8'))[0][0]
        print('Email Error: ', get_link)
        
        app_info['msg_data']['name'] = 'Auth Error'
        app_info['msg_data']['msg'] = f'Username and password not accepted.'
        app_info['msg_data']['help_link'] = get_link
        app_info['msg_data']['type'] = 'success'
        app_info['msg_data']['display'] = 'show'
        return False

# otp page
def otp_page(request):
    print('Verify for: ', app_info['verify_for'])
    return render(request,'app/otp_page.html', app_info)

# otp verify functionality
def verify_otp(request, verify_for='reg'):
    if request.method == 'POST':
        if int(request.POST['otp']) == request.session['otp']:
            master = Master.objects.get(Email=request.session['email'])
            
            if verify_for == 'rec':
                master.Password = request.POST['password']
                app_info['msg_data']['name'] = 'Password Changed'
                app_info['msg_data']['msg'] = 'Congratulations!! Your password has successfully changed.'
            else:
                master.IsActive = True
                if master.Role.Role == 'user':
                    User.objects.create(Master=master)
                elif master.Role.Role == 'doctor':
                    Doctor.objects.create(Master=master)
                elif 'pet' in master.Role.Role:
                    PetCareTaker.objects.create(Master=master)
                
                app_info['msg_data']['name'] = 'Verified'
                app_info['msg_data']['msg'] = 'Congratulations!! Your email has successfully verified.'

            master.save()

            app_info['msg_data']['type'] = 'success'
            app_info['msg_data']['display'] = 'show'

            del request.session['otp']
            del request.session['email']
            
            return redirect(login_page)
        else:
            app_info['msg_data']['name'] = 'Invalid OTP'
            app_info['msg_data']['msg'] = "OTP does not matched. Please enter correct otp."
            app_info['msg_data']['type'] = 'warning'
            app_info['msg_data']['display'] = 'show'
            return redirect(otp_page)
    else:
        app_info['msg_data']['name'] = 'Invalid Request'
        app_info['msg_data']['msg'] = "Something went wrong. Please try again leter."
        app_info['msg_data']['type'] = 'warning'
        app_info['msg_data']['display'] = 'show'
        return redirect(otp_page)
    pass
      
# load all roles
def load_role():
    all_role = Role.objects.all()
    return all_role

app_info['all_roles'] = load_role()
app_info['all_specialization'] = []
for sp in speciailization:
    app_info['all_specialization'].append({'short_tag': sp[0], 'tag': sp[1]})

# register page
def register_page(request):
    return render(request, 'app/register.html', app_info)

# register functionality
def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        role_id = int(request.POST['role'])
        password = request.POST['password']
        try:
            role = Role.objects.get(id=role_id)
            Master.objects.create(Email=email,Role=role,Password=password)

            request.session['email'] = email
            
            on_success = send_otp(request)
            
            if on_success:
                app_info['msg_data']['name'] = 'OTP Sent'
                app_info['msg_data']['msg'] = f'One-Time Password has sent to {email}.'
                app_info['msg_data']['type'] = 'success'
                app_info['msg_data']['display'] = 'show'
                
                return redirect(otp_page)
            else:
                return redirect(register_page)

        except IntegrityError as err:
            msg = f'Error in register view @ line 174: {err}'
            print(msg)
            console(err) # display error in terminal
            print('unique'.upper() in err.args[0])
            
            if 'unique'.upper() in err.args[0]:
                app_info['msg_data']['name'] = 'Email existed'
                app_info['msg_data']['msg'] = f'{email} is already existed.'

            app_info['msg_data']['type'] = 'danger'
            app_info['msg_data']['display'] = 'show'

            return redirect(register_page)
    else:
        pass

# login page
def login_page(request):
    return render(request, 'app/login.html', app_info)

# login functionality
@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        master = ''
        try:
            master =  Master.objects.get(Email=email)
            print(password, master.Password)
            role = master.Role
            print(role.Role)
            if master.Password != password:
                raise Exception('password does not matched.')
            else:
                request.session['email'] = email

            return redirect(index)
        except Master.DoesNotExist as err:
            console(err) # display error in terminal
            print('not exist' in err.args[0])
            
            if 'not exist' in err.args[0]:
                app_info['msg_data']['name'] = 'Not Registered'
                app_info['msg_data']['msg'] = f'{email} is not registered.'

            app_info['msg_data']['type'] = 'warning'
            app_info['msg_data']['display'] = 'show'
            return redirect(login_page)
        except Exception as err:
            console(err) # display error in terminal
            if master.Password != password:
                app_info['msg_data']['name'] = 'Wrong Password'
                app_info['msg_data']['msg'] = f'Your {err.args[0]}'

                app_info['msg_data']['type'] = 'warning'
                app_info['msg_data']['display'] = 'show'
            return redirect(login_page)
    else:
        pass

# forgot password page
def forgot_pass_page(request):
    return render(login_page)

# forgot password functionality
@csrf_exempt
def forgot_pass(request):
    if request.method == 'POST':
        email_to = request.session['email'] = request.POST['email']

        on_success = send_otp(request, otp_for='rec')

        if on_success:
            app_info['msg_data']['name'] = 'OTP Sent'
            app_info['msg_data']['msg'] = f'One-Time Password has sent to {email_to} for verification.'
            app_info['msg_data']['type'] = 'success'
            app_info['msg_data']['display'] = 'show'

            return redirect(otp_page)
        else:
            return redirect(login_page)
    else:
        pass


# load specializations
def load_specifications(doctor):
    return Specialization.objects.filter(Doctor=doctor)

# load specializations
def load_experience(doctor):
    exp_data = Experience.objects.filter(Doctor=doctor)
    for exp in exp_data:
        exp.DateFrom = exp.DateFrom.strftime('%Y-%m-%d')
        exp.DateTo = exp.DateTo.strftime('%Y-%m-%d')
    
    return exp_data

# load clinics
def load_clinics(doctor):
    return Clinic.objects.filter(Doctor=doctor)

# load appointments
def load_appointments(user, user_role):
    if user_role == 'doctor':
        return Appointment.objects.filter(Doctor=user)
    else:
        return Appointment.objects.filter(User=user)

from django.http import JsonResponse
# load clinics of selected doctor
def load_doctor_clinics(request):
    doctor = Doctor.objects.get(pk=int(request.POST.get('id')))
    dic = []
    clinics = Clinic.objects.filter(Doctor=doctor)
    for c in clinics:
        dic.append({'id':c.id, 'name':c.Name})

    return JsonResponse({'clinics': dic})

# load doctors data
def load_doctors():
    return Doctor.objects.all()

# load pet care takers
def load_petcaretakers():
    return PetCareTaker.objects.all()

# load all services added by pet care taker
def load_services(pk):
    all_services = Service.objects.filter(PetCareTaker=pk)
    for s in all_services:
        print(s.Name)
        for i in app_info['pet_service_names']:
            if s.Name == i['short_tag']:
                s.Name = i['tag']
    return all_services

# load all bookings from pet owner
def load_bookings(pk):
    bookings = Booking.objects.filter(PetCareTaker=pk)
    print(bookings)
    for s in bookings:
        print(s.Master)
        #for i in app_info['pet_service_names']:
        #    if s.PetDetail.Name == i['short_tag']:
        #        s.PetDetail.Name = i['tag']
    return bookings

# set status on bookings
def set_booking_status(request, booking_id, status):
    print(booking_id, status)
    master =  Master.objects.get(Email=request.session['email'])
    pet_care = PetCareTaker.objects.get(Master=master)
    booking = Booking.objects.get(pk=booking_id, PetCareTaker=pet_care)
    print(booking)
    booking.Status = status
    booking.save()

    return redirect(profile_page)

# set status on appointments
def set_appointment_status(request, appointment_id, status):
    print(appointment_id, status)
    master =  Master.objects.get(Email=request.session['email'])
    doctor = Doctor.objects.get(Master=master)
    appointment = Appointment.objects.get(pk=appointment_id, Doctor=doctor)
    print(appointment)
    appointment.Status = status
    appointment.save()

    return redirect(profile_page)

# get profile data
def profile_data(request):
    print(request.session['email'])
    if 'email' in request.session:
        try:
            master =  Master.objects.get(Email=request.session['email'])
            user_role = ''.join(master.Role.Role.split())
            print(user_role)
            app_info['user_role'] = user_role
            if user_role == 'user':
                user = User.objects.get(Master=master)
                app_info['profile_data'] = user
                app_info['pet_data'] = PetDetail.objects.filter(Master=master)
                app_info['doctors'] = load_doctors()
                app_info['petcaretakers'] = load_petcaretakers()
                app_info['symptoms'] = pet_symtops
                app_info['all_appointments'] = load_appointments(user, user_role)[::-1]
                app_info['all_bookings'] = Booking.objects.filter(Master=master)
                app_info['all_breeds'] = [] 
                for i in pet_breeds:
                    app_info['all_breeds'].append({'pet': i, 'breed': ','.join(pet_breeds[i])})
                print(app_info['all_breeds'])
            elif user_role == 'doctor':
                doctor = Doctor.objects.get(Master=master)
                app_info['profile_data'] = doctor
                app_info['profile_data'].DOB = app_info['profile_data'].DOB.strftime('%Y-%m-%d')
                app_info['education'] = Education.objects.filter(Doctor=doctor)
                app_info['experience'] = load_experience(doctor)
                app_info['specialization'] = load_specifications(doctor)
                app_info['clinic'] = load_clinics(doctor)[::-1]
                app_info['all_appointments'] = load_appointments(doctor, user_role)[::-1]
            elif user_role == 'petcaretaker':
                pet_care_data = PetCareTaker.objects.get(Master=master)
                app_info['profile_data'] = pet_care_data
                app_info['all_services'] = load_services(pet_care_data.pk)[::-1]
                app_info['all_bookings'] = load_bookings(pet_care_data)[::-1]

            if app_info['profile_data'].Image.url.split('/')[-1] != 'avtar.jpg':
                app_info['has_profile_image'] = True
            else:
                app_info['has_profile_image'] = False
        except Exception as err:
            print('Error in profile_data method @ line 189', err)

# profile page
def profile_page(request):
    profile_data(request)
    return render(request, 'app/profile.html', app_info)

# profile update
def profile_update(request):
    master = Master.objects.get(Email=request.session['email'])
    user = ''
    user_role = ''.join(master.Role.Role.split())
    if user_role == 'user':
        user = User.objects.get(Master=master)
    elif user_role == 'doctor':
        user = Doctor.objects.get(Master=master)
        user.About = request.POST['about']
        user.DOB = request.POST['dob']
    elif user_role == 'petcaretaker':
        user = PetCareTaker.objects.get(Master=master)
    
    user.FullName = request.POST['fullname']
    user.Mobile = request.POST['mobile']
    user.Gender = request.POST['gender']
    user.Country = request.POST['country']
    user.State = request.POST['state']
    user.City = request.POST['city']
    user.Pincode = request.POST['pincode']
    user.Address = request.POST['address']

    if 'user_image' in request.FILES:
        #user.Image = request.FILES['user_image']
        user_image = request.FILES['user_image']
        
        # renaming the uploaded image according to user id
        user_name = '_'.join(user.FullName.split())
        user_image.name = f'{user_role}_{user_name.lower()}.{user_image.name.split(".")[-1]}'

        for fname in os.listdir(user_image_path):
            if fname == user_image.name:
                f = os.path.join(user_image_path, user_image.name)
                print(f)
                os.remove(f)
                print(f"file {f} is deleted successfully")

        user.Image = user_image
    user.save()
    
    app_info['msg_data']['name'] = 'Profile Updated'
    app_info['msg_data']['msg'] = f'Your profile has been successfully updated.'
    app_info['msg_data']['type'] = 'success'
    app_info['msg_data']['display'] = 'show'
    return redirect(profile_page)

# change password
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']

        master = Master.objects.get(Email=request.session['email'])

        if current_password == master.Password:
            master.Password = new_password
            master.save()
            app_info['msg_data']['name'] = 'Password Changed'
            app_info['msg_data']['msg'] = f'Your password changed successfully done.'
            app_info['msg_data']['type'] = 'success'
        else:
            app_info['msg_data']['name'] = 'Not Matched'
            app_info['msg_data']['msg'] = f'Please enter your currect current password.'
            app_info['msg_data']['type'] = 'warning'
        app_info['msg_data']['display'] = 'show'
        return redirect(profile_page)
    else:
        pass

# doctor education update
def education_update(request):
    master = Master.objects.get(Email=request.session['email'])
    doctor = Doctor.objects.get(Master=master)
    degree = request.POST['degree']
    college = request.POST['college']
    endyear = request.POST['endyear']
    Education.objects.create(Doctor=doctor, Degree=degree, College=college, EndYear=endyear)
    
    app_info['msg_data']['name'] = 'Profile Updated'
    app_info['msg_data']['msg'] = f'Your profile has been successfully updated.'
    app_info['msg_data']['type'] = 'success'
    app_info['msg_data']['display'] = 'show'
    return redirect(profile_page)

# remove education
def remove_education(request, pk):
    Education.objects.get(pk=pk).delete()
    return redirect(profile_page)

# doctor experience update
def experience_update(request):
    master = Master.objects.get(Email=request.session['email'])
    doctor = Doctor.objects.get(Master=master)
    hospital = request.POST['hospital']
    designation = request.POST['designation']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    Experience.objects.create(
        Doctor = doctor,
        HospitalName = hospital,
        Designation = designation,
        DateFrom = start_date,
        DateTo = end_date
    )
    app_info['msg_data']['name'] = 'Profile Updated'
    app_info['msg_data']['msg'] = f'Your profile has been successfully updated.'
    app_info['msg_data']['type'] = 'success'
    app_info['msg_data']['display'] = 'show'
    return redirect(profile_page)

# remove experience
def remove_experience(request, pk):
    Experience.objects.get(pk=pk).delete()
    return redirect(profile_page)

# doctor specialization update
def specialization_update(request):
    master = Master.objects.get(Email=request.session['email'])
    doctor = Doctor.objects.get(Master=master)
    
    speciailization = request.POST['specification']
    
    Specialization.objects.create(
        Doctor=doctor,
        Tag = speciailization
    )
    
    app_info['msg_data']['name'] = 'Profile Updated'
    app_info['msg_data']['msg'] = f'Your profile has been successfully updated.'
    app_info['msg_data']['type'] = 'success'
    app_info['msg_data']['display'] = 'show'
    return redirect(profile_page)

# remove specialization
def remove_specialization(request, pk):
    Specialization.objects.get(pk=pk).delete()
    return redirect(profile_page)

# clinic update
def clinic_update(request):
    master = Master.objects.get(Email=request.session['email'])
    doctor = Doctor.objects.get(Master=master)
    name = request.POST['clinic_name']
    address = request.POST['clinic_address']

    clinic = Clinic.objects.create(
        Doctor = doctor,
        Name = name,
        Address = address
    )

    if 'clinic_image' in request.FILES:
        clinic.Image = request.FILES['clinic_image']
        clinic.save()

    app_info['msg_data']['name'] = 'Profile Updated'
    app_info['msg_data']['msg'] = f'Your profile has been successfully updated.'
    app_info['msg_data']['type'] = 'success'
    app_info['msg_data']['display'] = 'show'
    return redirect(profile_page)

# remove specialization
def remove_clinic(request, pk):
    Clinic.objects.get(pk=pk).delete()
    return redirect(profile_page)

app_info['year_month'] = []
for year_month in pet_age_term_choices:
    app_info['year_month'].append({'short_tag': year_month[0], 'tag': year_month[1]})

app_info['pet_gender'] = []
for gender in gender_choice:
    app_info['pet_gender'].append({'short_tag': gender[0], 'tag': gender[1]})

app_info['pet_service_names'] = []
for service in service_name_choices:
    app_info['pet_service_names'].append({'short_tag': service[0], 'tag': service[1]})

app_info['pet_type'] = pet_breeds.keys()
app_info['pet_breeds'] = pet_breeds

# add services by pet care taker
def add_service(request):
    service_name = request.POST['service']
    description = request.POST['description']
    is_active = False
    if 'isServiceActive' in request.POST:
        is_active = True

    master = Master.objects.get(Email=request.session['email'])
    pet_care_taker = PetCareTaker.objects.get(Master=master)

    new_service = Service.objects.create(
        PetCareTaker = pet_care_taker,
        Name=service_name,
        Description=description,
        IsActive = is_active
    )
    if 'service_image' in request.FILES:
        new_service.Image = request.FILES['service_image']
        new_service.save()

    app_info['msg_data']['name'] = 'Service Added'
    app_info['msg_data']['msg'] = f'New service added successfully.'
    app_info['msg_data']['type'] = 'success'
    app_info['msg_data']['display'] = 'show'
    return redirect(profile_page)

# create pet list by pet owner
def create_pet_list(request):
    petname = request.POST['petname']
    petage = request.POST['petage']
    year_month = request.POST['year_month']
    pet_type = request.POST['pet_type']
    pet_breed = request.POST['pet_breed']
    pet_gender = request.POST['pet_gender']

    master = Master.objects.get(Email=request.session['email'])

    PetDetail.objects.create(
        Master=master,
        Type=pet_type,
        Breed=pet_breed,
        Name=petname,
        Age=petage,
        YearMonth=year_month,
        Gender=pet_gender
    )

    app_info['msg_data']['name'] = 'Pet Added.'
    app_info['msg_data']['msg'] = f'Pet has been successfully added to pet list.'
    app_info['msg_data']['type'] = 'success'
    app_info['msg_data']['display'] = 'show'
    return redirect(profile_page)

# remove pet detail
def remove_pet_detail(request, pk):
    PetDetail.objects.get(pk=pk).delete()
    return redirect(profile_page)

# remove appointment
def remove_appointment(request, pk):
    Appointment.objects.get(pk=pk).delete()
    return redirect(profile_page)

# remove appointment
def remove_booking(request, pk):
    Booking.objects.get(pk=pk).delete()
    return redirect(profile_page)

# remove services by pet care taker
def remove_service(request, pk):
    Service.objects.get(pk=pk).delete()
    return redirect(profile_page)

# booking history
def booking_history(request):
    master = Master.objects.get(Email=request.session['email'])
    bookings = Booking.objects.filter(Master=master)
    
    dic = []

    for booking in bookings:
        for i in service_name_choices:
            if booking.Service.Name in i[0]:
                booking.Service.Name = i[1]
        #print(booking)
        
        dic.append(
            {
                'id': booking.id,
                #'pet_owner': pet_owner,
                'service': {'s_id': booking.Service.id, 's_name': booking.Service.Name},
                'pet_care_taker': {'ptc_id': booking.PetCareTaker.id, 'ptc_name': booking.PetCareTaker.FullName},
                'pets': {'pet_id': booking.PetDetail.id, 'pet_name': booking.PetDetail.Name},
                'date_time': booking.Date.strftime('%Y-%m-%d'),
                'status': booking.Status,
            }
        )

    return JsonResponse({'booking_history': dic[::-1]})

# appointment history
def appointment_history(request):
    pass

# logout
def logout(request):
    if 'email' in request.session:
        del request.session['email']
        app_info['profile_data'] = ''
    return redirect(index)

# make doctor appointment page
def make_appointment_page(request):
    return render(request, 'app/doctor_booking.html', app_info)

# make appointment functionality
def make_appointment_old(request, pk):
    master = Master.objects.get(Email=request.session['Email'])
    user = User.objects.get(Master=master)
    doctor = Doctor.objects.get(id=pk)
    appointment_request_list = request.POST
    for u in appointment_request_list:
        
        for pet_id in u['pets']:
            pet = PetDetail.objects.get(id=pet_id)

            Appointment.objects.create(
                User = user,
                Doctor = doctor,
                PetDetail = pet,
                HealthIssue = ','.join(u['symptoms'])
            )

# load selected pet care services by user
def load_ptc_services(request):
    pet_care_taker = PetCareTaker.objects.get(pk=int(request.POST.get('id')))
    dic = []
    services = Service.objects.filter(PetCareTaker=pet_care_taker,IsActive=True)
    for service in services:
        for i in app_info['pet_service_names']:
            if service.Name == i['short_tag']:
                service.Name = i['tag']
        dic.append({'id':service.id, 'name':service.Name})

    return JsonResponse({'services': dic})


# book service functionality
def book_service(request):
    master = Master.objects.get(Email=request.session['email'])

    booking_request_list = request.POST

    pet_care_taker_id = int(booking_request_list['pet_care_taker'])
    pet_care_taker = PetCareTaker.objects.get(id=pet_care_taker_id)

    pet_list = booking_request_list.getlist('pet_list')
    service_list = booking_request_list.getlist('service_list')
    
    for pet_id in pet_list:
        #print(pet_id, type(int(pet_id)))
        pet = PetDetail.objects.get(id = pet_id)
        #print('pet, ', pet)
        for s_id in service_list:
            service = Service.objects.get(id=s_id, PetCareTaker=pet_care_taker )

            Booking.objects.create(
                Master = master,
                PetDetail = pet,
                PetCareTaker = pet_care_taker,
                Service = service
            )
    
    app_info['msg_data']['name'] = 'Booked'
    app_info['msg_data']['msg'] = f'Your booking has been successfully updated.'
    app_info['msg_data']['type'] = 'success'
    app_info['msg_data']['display'] = 'show'
    return redirect(profile_page)

# make appointment functionality
def make_appointment(request):
    master = Master.objects.get(Email=request.session['email'])
    user = User.objects.get(Master=master)
    appointment_request_list = request.POST
    doctor = Doctor.objects.get(id=int(request.POST['doctor_id']))

    pet_list = appointment_request_list.getlist('pet_list')
    symptoms_list = appointment_request_list.getlist('symptoms_list')

    print(pet_list, symptoms_list)

    #for u in appointment_request_list:
    for pet_id in pet_list:
        pet = PetDetail.objects.get(id=int(pet_id))
        #print(pet)
        for sym in symptoms_list:
            Appointment.objects.create(
                User = user,
                Doctor = doctor,
                PetDetail = pet,
                Symptoms = sym
            )
    
    app_info['msg_data']['name'] = 'Appointment Scheduled'
    app_info['msg_data']['msg'] = f'Your appointment has been successfully scheduled.'
    app_info['msg_data']['type'] = 'success'
    app_info['msg_data']['display'] = 'show'
    return redirect(profile_page)
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('about/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
    path('logout/', logout, name='logout'),

    # REGISTER PAGE AND FUNCTIONALITY
    path('register_page/', register_page, name='register_page'),
    path('register/', register, name='register'),

    # LOGIN PAGE AND FUNCTIONALITY
    path('login_page/', login_page, name='login_page'),
    path('login/', login, name='login'),

    # FORGOT PASSWORD PAGE AND FUNCTIONALITY
    path('forgot_pass_page/', forgot_pass_page, name='forgot_pass_page'),
    path('forgot_pass/', forgot_pass, name='forgot_pass'),

    # SEND OTP, OTP PAGE, VERIFIY OTP AND FUNCTIOALITY
    path('otp_page/', otp_page, name='otp_page'), 
    #path('verify_otp/', verify_otp, name='verify_otp'),
    path('verify_otp/<str:verify_for>/',verify_otp, name='otp_verify'),
    
    # PROFILE PAGE AND UPDATE FUNCTIOALITY
    path('profile_page/', profile_page, name='profile_page'), 
    path('profile_update/', profile_update, name='profile_update'),
    path('change_password/', change_password, name='change_password'),
    path('load_dr_clinic/', load_doctor_clinics, name='load_dr_clinic'),
    
    path('create_pet_list/', create_pet_list, name='create_pet_list'),
    path('remove_pet_detail/<int:pk>/', remove_pet_detail, name='remove_pet_detail'),
    path('booking_history/', booking_history, name='booking_history'),

    # PET CARE SERVICE
    path('add_service/', add_service, name='add_service'),
    path('remove_service/<int:pk>/', remove_service, name='remove_service'),
    path('set_booking_status/<int:booking_id>/<str:status>/', set_booking_status, name='set_booking_status'),

    # DOCTOR 
    path('education_update/', education_update, name='education_update'),
    path('remove_education/<int:pk>/', remove_education, name='remove_education'),
    path('experience_update/', experience_update, name='experience_update'),
    path('remove_experience/<int:pk>/', remove_experience, name='remove_experience'),
    path('specialization_update/', specialization_update, name='specialization_update'),
    path('remove_specialization/<int:pk>/', remove_specialization, name='remove_specialization'),
    path('clinic_update/', clinic_update, name='clinic_update'),
    path('remove_clinic/<int:pk>/', remove_clinic, name='remove_clinic'),
    path('set_appointment_status/<int:appointment_id>/<str:status>/', set_appointment_status, name='set_appointment_status'),

    # MAKE APPOINTMENT PAGE AND FUNCTIONALITY
    #path('make_appointment_page/', make_appointment_page, name='make_appointment_page'),
    path('make_appointment/', make_appointment, name='make_appointment'),
    path('remove_appointment/<int:pk>/', remove_appointment, name='remove_appointment'),
    path('load_ptc_services/', load_ptc_services, name='load_ptc_services'),

    # BOOK SERVICE PAGE AND FUNCTIONALITY
    path('book_service/', book_service, name='book_service'),
    path('remove_booking/<int:pk>/', remove_booking, name='remove_booking'),

]
from django.contrib import admin
from .views import app_info
from .models import *

class SuperAdmin(admin.ModelAdmin):
    admin.site.site_header = admin.site.site_title = app_info['app_name']
    admin.site.index_title = f"{app_info['app_name']}'s Admin"
    empty_value_display = '-empty-'
    list_per_page = 10

class RoleAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('id', 'Role')
    list_filter = list_display
    
    
class MasterAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('id', 'Email', 'Role')
    list_filter = list_display
    
class AppointmentAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('User', 'Doctor', 'PetDetail', 'Symptoms', 'Status')
    list_filter = list_display
    
class ClinicAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('Doctor', 'Name')
    list_filter = list_display
    
class ServiceAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('PetCareTaker', 'Name', 'IsActive')
    list_filter = list_display
    
class SpecializationAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('Doctor', 'Tag')
    list_filter = list_display
    
class ExperienceAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('Doctor', 'HospitalName', 'Designation')
    list_filter = list_display

models_list = [ User, PetDetail, Doctor, Education, PetCareTaker, Booking, Feedback]

roles = ['user','doctor','pet care taker']
if not len(Role.objects.all()):
    for role in roles:
        Role.objects.create(Role=role)
        
for model in models_list:
    admin.site.register(model, SuperAdmin)

admin.site.register(Role, RoleAdmin)
admin.site.register(Master, MasterAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Clinic, ClinicAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(Experience, ExperienceAdmin)
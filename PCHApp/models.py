from django.db import models
from django.core.validators import MinValueValidator
gender_choice = (
    ('m', 'Male'),
    ('f', 'Female'),
)

class Role(models.Model):
    Role = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'Role'

    def __str__(self):
        return self.Role

class Master(models.Model):
    Role = models.ForeignKey(Role, on_delete=models.CASCADE)
    Email = models.EmailField(max_length=50, unique=True)
    Password = models.CharField(max_length=50)
    IsActive = models.BooleanField(default=False)
    DateCreated = models.DateTimeField(auto_now_add=True)
    DateUpdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Master'

    def __str__(self):
        return self.Email

class User(models.Model):
    Master = models.ForeignKey(Master,on_delete=models.CASCADE)
    Image = models.FileField(upload_to="image/users/", default="avtar.jpg")
    FullName = models.CharField(max_length=50, default='')
    Mobile = models.CharField(max_length=10, default='')
    Gender = models.CharField(max_length=50, choices=gender_choice)
    Address = models.TextField(max_length=50, default='')
    Country = models.CharField(max_length=20, default='')
    State = models.CharField(max_length=20, default='')
    City = models.CharField(max_length=20, default='')
    Pincode = models.CharField(max_length=6, default='')

    class Meta:
        db_table = 'User'

    def __str__(self):
        return self.Master.Email

from .symptoms import pet_symtops
symptoms = []
for i in pet_symtops:
    symptoms.append((i, i))
    
symptoms = tuple(symptoms)

pet_breeds = {
    'dog': ['Labrador Retriever', 'Golden Retriever', 'Bernese Mountain Dog','Scotch (Rough) Collie','Great Dane','Newfoundland'],
    'fish': [],
    'rabbit': [],
    'turtle': [],
    'cat': []
}
pet_type_choices = []
for t in pet_breeds.keys():
    pet_type_choices.append( (t, t.capitalize()) )

pet_type_choices = tuple(pet_type_choices)


pet_age_term_choices = (
    ('mon', 'Month'),
    ('yr', 'Year'),
)

class PetDetail(models.Model):
    Master = models.ForeignKey(Master, on_delete=models.CASCADE) # for user and doctor
    Type = models.CharField(max_length=50, choices=pet_type_choices)
    Breed = models.CharField(max_length=50, default='')
    Name = models.CharField(max_length=50, default='')
    Age = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    YearMonth = models.CharField(max_length=50, choices=pet_age_term_choices)
    Gender = models.CharField(max_length=50, choices=gender_choice)

    class Meta:
        db_table = 'PetDetail'

    def __str__(self):
        return self.Name

class PetCareTaker(models.Model):
    Master = models.ForeignKey(Master,on_delete=models.CASCADE)
    Image = models.FileField(upload_to="image/pet-takers/", default="avtar.jpg")
    FullName = models.CharField(max_length=50, default='')
    Mobile = models.CharField(max_length=10, default='')
    Gender = models.CharField(max_length=50, choices=gender_choice)
    Address = models.TextField(max_length=50, default='')
    Country = models.CharField(max_length=20, default='')
    State = models.CharField(max_length=20, default='')
    City = models.CharField(max_length=20, default='')
    Pincode = models.CharField(max_length=6, default='')

    class Meta:
        db_table = 'PetCareTaker'

    def __str__(self):
        return self.FullName

speciailization = (
    ('skin', 'Skin'),
    ('ortho', 'Orthopadic'),
)
import datetime
class Doctor(models.Model):
    Master = models.ForeignKey(Master,on_delete=models.CASCADE)
    # personal info
    Image = models.FileField(upload_to="image/doctors/", default="avtar.jpg")
    FullName = models.CharField(max_length=50, blank=True)
    DOB = models.DateField(default=datetime.datetime.now())
    Mobile = models.CharField(max_length=10, blank=True)
    Gender = models.CharField(max_length=50, choices=gender_choice)
    About = models.TextField(max_length=5000, blank=True)
    
    # contact info
    Address = models.TextField(max_length=100, blank=True)
    Country = models.CharField(max_length=20, blank=True)
    State = models.CharField(max_length=20, blank=True)
    City = models.CharField(max_length=20, blank=True)
    Pincode = models.CharField(max_length=6, blank=True)

    class Meta:
        db_table = 'Doctor'     
        

    def __str__(self):
        return self.Master.Email

    #def __str__(self):
    #    return self.DOB.strftime('%Y%m%d')

class Clinic(models.Model):
    Doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100)
    Address = models.TextField(max_length=300)
    Image = models.FileField(upload_to="image/clinics/", default="avtar.jpg")

    class Meta:
        db_table = 'Clinic'

    def __str__(self):
        return self.Doctor.Master.Email

class Education(models.Model):
    # academic info
    Doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    Degree = models.CharField(max_length=50)
    College = models.CharField(max_length=50)
    EndYear = models.CharField(max_length=4)

    class Meta:
        db_table = 'Education'

class Specialization(models.Model):
    # professional info
    Doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    Tag = models.CharField(max_length=50, choices=speciailization)

    class Meta:
        db_table = 'Specialization'

class Experience(models.Model):
    Doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    HospitalName = models.CharField(max_length=20)
    Designation = models.CharField(max_length=50)
    DateFrom = models.DateField()
    DateTo = models.DateField()

    class Meta:
        db_table = 'Experience'

class Appointment(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    PetDetail = models.ForeignKey(PetDetail, on_delete=models.CASCADE)
    DateTime = models.DateTimeField(auto_now=True)
    Symptoms = models.CharField(max_length=70, choices=symptoms)
    Status = models.CharField(max_length=50,default="pending")

    class Meta:
        db_table = 'Appointment'

    def __str__(self):
        return f'{self.User.FullName} - {self.Doctor.FullName} - {self.PetDetail.Name} - {self.Symptoms}'

service_name_choices = (
    ('grm', 'grooming'),
    ('trn', 'trainning'),
    ('dc', 'day camp'),
    ('brd', 'pet boarding')
)
class Service(models.Model):
    PetCareTaker = models.ForeignKey(PetCareTaker, on_delete=models.CASCADE)
    Name = models.CharField(max_length=70, choices=service_name_choices)
    Image = models.FileField(upload_to="image/services/", default="service.jpg")
    Description = models.TextField(max_length=20000)
    IsActive = models.BooleanField(default=False)

    class Meta:
        db_table = 'Service'
    
    def __str__(self):
        self.name = ''
        for i in service_name_choices:
            if self.Name in i[0]:
                self.name = i[1]
        return self.name.capitalize()

class Booking(models.Model):
    Master = models.ForeignKey(Master, on_delete=models.CASCADE) # for user and doctor
    PetDetail = models.ForeignKey(PetDetail, on_delete=models.CASCADE)
    PetCareTaker = models.ForeignKey(PetCareTaker, on_delete=models.CASCADE)
    Service = models.ForeignKey(Service, on_delete=models.CASCADE)
    Date = models.DateTimeField(auto_now=True)
    Status = models.CharField(max_length=50,default="pending")

    class Meta:
        db_table = 'Booking'

class Feedback(models.Model):
    Master = models.ForeignKey(Master, on_delete=models.CASCADE)
    PetCareTaker = models.ForeignKey(PetCareTaker,on_delete=models.CASCADE)
    Name = models.CharField(max_length=50)
    Email = models.EmailField(max_length=50)
    Review = models.CharField(max_length=2000)

    class Meta:
        db_table = 'Feedback'
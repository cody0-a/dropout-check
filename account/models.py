from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('principal', 'Principal'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    sex = models.CharField(max_length=1, choices=[('F', 'Female'), ('M', 'Male')])

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    sex = models.CharField(max_length=1, choices=[('F', 'Female'), ('M', 'Male')])
    image = models.ImageField(upload_to='photos/',width_field=300,height_field=400)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateTimeField(null=False,auto_now=True, auto_now_add=False)

class Student(models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='list_student')
    roll_no = models.CharField(max_length=10)
    batch = models.CharField(max_length=4)
    section = models.CharField(max_length=1)
    semester = models.IntegerField()
    dropout = models.BooleanField(default=False)
    dropout_reason = models.TextField(null=True, blank=True)

    class Meta:
        permissions = [
            ('can_add_student', 'Can add student'),
            ('can_change_student', 'Can change student'),
            ('can_delete_student', 'Can delete student'),
            ('can_view_student', 'Can view student'),
        ]

    def __str__(self):
        return self.user.username
    
    # other fields

class SchoolAddress(models.Model):
    SchoolName =models.ForeignKey('SchoolName',on_delete=models.DO_NOTHING,related_name='school_address_name')
    wereda_name = models.CharField(max_length=100)
    street_name = models.CharField(max_length=100,default='unknown'.title())
    city = models.CharField(max_length=100,default='unknown'.title())
    state = models.CharField(max_length=100,default='unknown'.title())
    region = models.CharField(max_length=64)
    zone_id = models.CharField(max_length=64)
    school_code = models.CharField(max_length=64)

    def __str__(self):
        return self.wereda_name


class SchoolName(models.Model):
    name = models.CharField(max_length=100)
    address = models.ForeignKey(SchoolAddress,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField()
    logo = models.ImageField(upload_to='school_logo')
    motto = models.TextField()
    about = models.TextField()
    principal = models.CharField(max_length=100)
    vice_principal = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name
    

class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher')
    school = models.ForeignKey(SchoolName, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    qualification = models.TextField()
    experience = models.TextField()
    date_of_join = models.DateTimeField(auto_now=True, auto_now_add=False)
    profile_pic = models.ImageField(upload_to='teacher_profile')
    phone = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateTimeField()

    def __str__(self):
        return self.user.username
    
class Parent(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='parent')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateTimeField()

    def __str__(self):
        return self.user.username
    
class DropOut(models.Model):
    DROP_OUT_CHOICES = [
        ('Academic', 'Academic'),
        ('Financial', 'Financial'),
        ('Health', 'Health'),
        ('Personal', 'Personal'),
        ('Marriage', 'Marriage'),
        ('Distance', 'Distance'),
        ('Death', 'Death'),
        ('Other', 'Other'),
    ]
    SEMESTER_CHOICE = [
        ('1st Semester', '1st Semester'),
        ('2nd Semester', '2nd Semester'),
    ]
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='dropout_student')
    reason = models.TextField()
    dropout_reason = models.CharField(max_length=100, choices=DROP_OUT_CHOICES)
    year = models.DateTimeField(auto_now=True, auto_now_add=False)
    semester = models.CharField(max_length=32,choices=SEMESTER_CHOICE)

    def __str__(self):
        return self.student.user.username
    
    
class DropoutSummary(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='dropout_summary')
    is_dropout = models.BooleanField(default=True)
    total_students = models.IntegerField(default=0)
    total_dropouts = models.IntegerField(default=0)
    academic_dropouts = models.IntegerField(default=0)
    financial_dropouts = models.IntegerField(default=0)
    health_dropouts = models.IntegerField(default=0)
    personal_dropouts = models.IntegerField(default=0)
    marriage_dropouts = models.IntegerField(default=0)
    distance_dropouts = models.IntegerField(default=0)
    death_dropouts = models.IntegerField(default=0)
    other_dropouts = models.IntegerField(default=0)

    def __str__(self):
        return "Dropout Summary"
    

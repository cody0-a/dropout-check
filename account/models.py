from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    sex = models.CharField(max_length=1, choices=[('F', 'Female'), ('M', 'Male')])


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    sex = models.CharField(max_length=1, choices=[('F', 'Female'), ('M', 'Male')])
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateTimeField(null=False,auto_now=True, auto_now_add=False)

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='list_student')
    roll_no = models.CharField(max_length=10)

    department = models.CharField(max_length=100)
    batch = models.CharField(max_length=4)
    section = models.CharField(max_length=1)
    semester = models.IntegerField()
    cgpa = models.FloatField()
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

class SchoolName(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField()
    logo = models.ImageField(upload_to='school_logo')
    established = models.DateField()
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
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='dropout_student')
    reason = models.TextField()
    DropOut_case = models.CharField(max_length=100, choices=[('Academic', 'Academic'), ('Financial', 'Financial'), ('Health', 'Health'), ('Personal', 'Personal'),('marriage', 'marriage'),('distance', 'distance'),
    ('death','death'),('other', 'other')])
    date = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.student.user.username
    

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField(auto_now=True, auto_now_add=False)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])
    reason = models.TextField(null=True, blank=True)


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
    

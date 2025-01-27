from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

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

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.user.username
class Student(models.Model):
    student_id =models.CharField(max_length=32) 
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='list_student')
    roll_no = models.CharField(max_length=10)
    batch = models.CharField(max_length=4)
    section = models.CharField(max_length=1)
    semester = models.IntegerField()
    dropout = models.BooleanField(default=False)
    dropout_reason = models.TextField(null=True, blank=True)

    @classmethod
    def total_student(cls) -> int:
        return cls.objects.count()
    

    class Meta:
        verbose_name = "student"
        verbose_name_plural = 'students'


        permissions = [
            ('can_add_student', 'Can add student'),
            ('can_change_student', 'Can change student'),
            ('can_delete_student', 'Can delete student'),
            ('can_view_student', 'Can view student'),
        ]


    def __str__(self):
        return self.user.username

    def save(self,*args,**kwargs):
        if not self.student_id:
            unique_id = self.user.username[0].upper() + str(self.user.id) + str(self.roll_no)
            self.student_id = unique_id 
            self.student_id = f"{self.student_id}"
            super(Student,self).save(*args,**kwargs)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('student-detail',kwargs={'pk':self.pk})
    
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


class SchoolProfile(models.Model):
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
    school = models.ForeignKey(SchoolProfile, on_delete=models.CASCADE)
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

    dropout_reason = models.CharField(max_length=100, choices=DROP_OUT_CHOICES)
    year = models.DateTimeField(auto_now=True, auto_now_add=False)
    semester = models.CharField(max_length=32,choices=SEMESTER_CHOICE)

    def __str__(self):
        return self.student.user.username
    
    def calculate_based_on_dropout(self):
        dropout_count = {reason[0] : 0 for reason in self.DROP_OUT_CHOICES}
        dropout_count[self.dropout_reason] += 1

        return dropout_count

    def semester_dropout(self):
        per_semester_dropout = {sem[0] : 0 for sem in self.SEMESTER_CHOICE}
        per_semester_dropout[self.semester] += 1

    


    
    
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
    
    def get_dropped(self):
        if self.is_dropout == True:
            total_dropout = (
                self.academic_dropouts + self.health_dropouts\
                + self.personal_dropouts + self.marriage_dropouts\
                + self.distance_dropouts + self.death_dropouts\
                + self.other_dropouts + self.financial_dropouts\
                
            )
            total_dropouts = self.total_students - total_dropout

            return total_dropouts
        else:
            return

    

        
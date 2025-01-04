from django.contrib import admin
from .models import UserProfile, Student, SchoolName, Teacher,CustomUser

@admin.register(UserProfile)    
class UserProfile(admin.ModelAdmin):
    pass


@admin.register(Student)
class Student(admin.ModelAdmin):
    pass

@admin.register(SchoolName)
class SchoolName(admin.ModelAdmin):
    pass

@admin.register(Teacher)
class Teacher(admin.ModelAdmin):
    pass

@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    pass


admin.site.site_header = "Korax School Management System"
admin.site.site_title = "Korax School Management System"
admin.site.index_title = "Welcome to Korax School Management System"







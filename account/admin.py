from django.contrib import admin
from .models import Student, SchoolProfile, Teacher,CustomUser,Profile
from django.contrib.auth import get_permission_codename

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_no', 'batch', 'section', 'semester', 'dropout')
    search_fields = ('user__username', 'roll_no', 'batch')
    list_filter = ('dropout', 'batch')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user__is_active=True)
        
    def has_add_permission(self, request):
        return request.user.has_perm('account_can_add_student')
    
    def has_delete_permission(self,request):
        return request.user.has_perm('account_can_delete_student')
    
    def has_change_permission(self,request):
        return request.user.has_perm('account_can_change_student')
    
    def has_view_permission(self, request):
        return request.user.has_perm('account_can_view_student')
    
    
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        else:
            return ('dropout',)
        
@admin.register(SchoolProfile)
class SchoolProfileAdmin(admin.ModelAdmin):
    list_filter =['name','phone','email']
    list_display = ('name','phone','email')
    search_fields = ('name','phone','email')
    
    def get_queryset(self, request):
        qs  = super().get_queryset(request)
        if request.user.is_active and request.user.is_staff:
            return qs
        else:
            return qs.filter(user__is_active=True)
        
        
@admin.register(Teacher)
class Teacher(admin.ModelAdmin):
    pass

@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    pass

admin.site.register(Profile)

admin.site.site_header = "Korax School Management System"
admin.site.site_title = "Korax School Management System"
admin.site.index_title = "Welcome to Korax School Management System"







from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.create_student, name='add'),
    path('login/', views.login_view, name='login'),
    path('register/',views.register,name='register'),
    path('category/',views.get_categories,name='category'),
    path('profile/',views.profile,name='profile'),
    path('update-profile/',views.update_profile,name='update_profile'),
    path('delete-profile/',views.delete_profile,name='delete_profile'),
    path('change-password/',views.change_password,name='change_password'),
    path('forgot-password/',views.forgot_password,name='forgot_password'),
    path('reset-password/',views.reset_password,name='reset_password'),
    path('students/', views.get_students, name='student'),
    #path('students/<int:id>/', views.get_student, name='student'),
    path('students/create/', views.create_student, name='create_student'),
    #path('students/update/<int:id>/', views.update_student, name='update_student'),
    #path('students/delete/<int:id>/', views.delete_student, name='delete_student'),
    path('students/search/', views.search_student, name='search_student'),
    path('students/filter/', views.filter_student, name='filter_student'),
    path('students/sort/', views.sort_student, name='sort_student'),
    path('students/export/', views.export_students, name='export_students'),
    path('students/import/', views.import_students, name='import_students'),
    path('students/upload/', views.upload_students, name='upload_students'),
    path('students/download/', views.download_students, name='download_students'),
    path('reports/', views.get_reports, name='reports'),
    path('users/', views.get_registered_users, name='users'),
    path('dropout-summary',views.dropout_summary,name='dropout_summary'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('settings/', views.get_settings, name='settings'),
    path('dropout_rate/', views.get_dropout_rate, name='dropout_rate'),
    path('categorized-students/', views.categorize_students, name='categorized_students'),
    path('edit-student/<int:student_id>', views.edit_student, name='edit_student'),
    path('logout/', views.logout_view, name='logout'),
]
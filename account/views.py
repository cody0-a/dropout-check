import openpyxl
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from .models import * 
from .models import UserProfile
from .forms import * 
from django.http import HttpResponse
from django.contrib import messages
User = get_user_model()

def home(request):
    return render(request, 'account/index.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a home page
        else:
            # Invalid login
            return render(request, 'account/login.html', {'error': 'Invalid credentials'})
    return render(request, 'account/login.html')



def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        sex = request.POST.get('sex')
        year = request.POST.get('year')
        month = request.POST.get('month')
        day = request.POST.get('day')

        # Validate passwords
        if password != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'account/register.html')

        # Check for existing username or email
        User = get_user_model()
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "Username or email is already taken.")
            return render(request, 'account/register.html')

        # Create a new user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        # Create date_of_birth from year, month, and day
        date_of_birth = f"{year}-{month.zfill(2)}-{day.zfill(2)}"  # Format to YYYY-MM-DD
        UserProfile.objects.create(user=user, sex=sex, date_of_birth=date_of_birth)

        # Log the user in
        login(request, user)
        messages.success(request, "Registration successful!")
        return redirect('users')

    return render(request, 'account/register.html')

def get_registered_users(request):
    users = User.objects.all()
    profiles = UserProfile.objects.all()
    user_data = [{
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'profile': {
            'sex': profile.sex,
            'date_of_birth': profile.date_of_birth,

        } if (profile := profiles.filter(user=user).first()) else {}
    } for user in users]

    return render(request, 'account/users.html', {'user_data': user_data})

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect


def register_student(request):
    if request.method == 'POST':
        user = request.user
        roll_no = request.POST.get('roll_no')
        department = request.POST.get('department')
        batch = request.POST.get('batch')
        section = request.POST.get('section')
        semester = request.POST.get('semester') 
        cgpa = request.POST.get('cgpa')
        dropout = request.POST.get('dropout')
        dropout_reason = request.POST.get('dropout_reason')

        # Other fields...

        # Create a new student
        student = Student.objects.create(
            fname=user.usernamefirst_name,
            lname=user.last_name,
            roll_no=roll_no,
            department=department,
            batch=batch,
            section=section,
            semester=semester,
            cgpa=cgpa,
            dropout=dropout,
            dropout_reason=dropout_reason
        )

        summary, created = DropoutSummary.objects.get_or_create(id=1)  # Assuming a single summary record
        summary.total_students += 1

        if student.dropout:
            summary.total_dropouts += 1
            if student.dropout_reason:
                summary.dropout_reason = student.dropout_reason
                if student.dropout_reason == "Academic":
                    summary.academic_dropouts += 1
                elif student.dropout_reason == "Financial":
                    summary.financial_dropouts += 1
                elif student.dropout_reason == "Health":
                    summary.health_dropouts += 1
                elif student.dropout_reason == "Personal":
                    summary.personal_dropouts += 1
                elif student.dropout_reason == "Marriage":
                    summary.marriage_dropouts += 1
                elif student.dropout_reason == "Distance":
                    summary.distance_dropouts += 1
                elif student.dropout_reason == "Death":
                    summary.death_dropouts += 1
                else:
                    summary.other_dropouts += 1

        summary.save()

        # Redirect or render as necessary
        return redirect('home')

    return render(request, 'account/register.html')


def dashboard(request):
    return render(request, 'account/dashboard.html')


def categorize_students(request):
    students = Student.objects.all()
    dropout_reasons = {
        "Academic": [],
        "Financial": [],
        "Health": [],
        "Personal": [],
        "Marriage": [],
        "Distance": [],
        "Death": [],
        "Other": []
    }

    for student in students:
        if student.dropout:
            dropout_reason = student.dropout_reason if student.dropout_reason else "Other"
            dropout_reasons[dropout_reason].append(student)

    return render(request, 'account/categorized_students.html', {'dropout_reasons': dropout_reasons})



@login_required
@permission_required('account.can_add_student', raise_exception=True)
def register_student(request):
    if request.method == 'POST':
        # Registration logic here
        return redirect('some_view')
    return render(request, 'account/register.html')


@login_required
@permission_required('account.can_change_student', raise_exception=True)
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    form = StudentForm(request.POST or None, instance=student)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('home')  # Redirect after saving

    return render(request, 'account/edit.html', {'form': form, 'student': student})


@permission_required('account.can_delete_student', raise_exception=True)
def delete_student(request, student_id):
    student = Student.objects.get(id=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('get_students')
    return render(request, 'account/delete.html', {'student': student})


@login_required
@permission_required('account.can_view_student', raise_exception=True)
def view_students(request):
    students = Student.objects.all()
    return render(request, 'account/view.html', {'students': students})


@login_required
@permission_required('account.can_view_student', raise_exception=True)
def view_student(request, student_id):
    student = Student.objects.get(id=student_id)
    return render(request, 'account/view.html', {'student': student})

@login_required
@permission_required('account.can_view_student', raise_exception=True)
def search_student(request):
    query = request.GET.get('query')
    students = Student.objects.filter(roll_no__icontains=query)
    return render(request, 'account/search.html', {'students': students})

@login_required
@permission_required('account.can_view_student', raise_exception=True)
def filter_student(request):
    department = request.GET.get('department')
    students = Student.objects.filter(department=department)
    return render(request, 'account/filter.html', {'students': students})

@login_required
@permission_required('account.can_view_student', raise_exception=True)
def sort_student(request):
    students = Student.objects.all().order_by('roll_no') 
    return render(request, 'account/sort.html', {'students': students})

@login_required
@permission_required('account.can_view_student', raise_exception=True)
def export_students(request):
    students = Student.objects.all()
    # Export logic here
    return redirect('home')

@login_required
@permission_required('account.can_view_student', raise_exception=True)
def import_students(request):
    if request.method == 'POST':
        # Import logic here
        return redirect('students')
    return render(request, 'account/import.html')

@login_required
@permission_required('account.can_view_student', raise_exception=True)
def upload_students(request):
    if request.method == 'POST':
        # Upload logic here
        return redirect('home')
    return render(request, 'account/upload.html')

@login_required
@permission_required('account.can_view_student', raise_exception=True)
def download_students(request):
    # Download logic here
    return redirect('download_students')


@login_required
@permission_required('account.can_view_student', raise_exception=True)
def get_reports(request):
    return redirect('home')


@login_required
@permission_required('account.can_edit_student', raise_exception=True)
def update_profile(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        # Update logic here
        return redirect('profile')
    return render(request, 'account/profile.html', {'profile': profile})

@login_required
@permission_required('account.can_view_student', raise_exception=True)
def view_profile(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    return render(request, 'account/profile.html', {'profile': profile})

@login_required
@permission_required('account.can_view_student', raise_exception=True)
def search_profile(request):
    query = request.GET.get('query')
    profiles = UserProfile.objects.filter(user__username__icontains=query)
    return render(request, 'account/search_profile.html', {'profiles': profiles})

@login_required
@permission_required('account.can_view_student', raise_exception=True)
def filter_profile(request):
    profile = request.GET.get('profile')
    profiles = UserProfile.objects.filter(profile=profile)
    return render(request, 'account/filter_profile.html', {'profiles': profiles})

@login_required
@permission_required('account.can_view_student', raise_exception=True)
def sort_profile(request):
    profiles = UserProfile.objects.all().order_by('user__username')
    return render(request, 'account/sort_profile.html', {'profiles': profiles})


@login_required
@permission_required('account.can_view_student', raise_exception=True)
def profile(request):
    return redirect('home')


@login_required
@permission_required('account.can_delete_student', raise_exception=True)
def delete_profile(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        profile.delete()
        return redirect('home')
    return render(request, 'account/delete_profile.html', {'profile': profile})

@login_required
def change_password(request):
    user = request.user
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')

        if not user.check_password(old_password):
            messages.error(request, "Incorrect old password.")
            return render(request, 'account/change_password.html')

        if new_password != new_password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'account/change_password.html')

        user.set_password(new_password)
        user.save()
        login(request, user)
        messages.success(request, "Password changed successfully!")
        return redirect('home')

    return render(request, 'account/change_password.html')


@login_required
def change_email(request):
    user = request.user
    if request.method == 'POST':
        email = request.POST.get('email')
        user.email = email
        user.save()
        messages.success(request, "Email changed successfully!")
        return redirect('home')

    return render(request, 'account/change_email.html')

@login_required
def change_username(request):
    user = request.user
    if request.method == 'POST':
        username = request.POST.get('username')
        user.username = username
        user.save()
        messages.success(request, "Username changed successfully!")
        return redirect('home')

    return render(request, 'account/change_username.html')

@login_required
def change_name(request):
    user = request.user
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        messages.success(request, "Name changed successfully!")
        return redirect('home')

    return render(request, 'account/change_name.html')


@login_required
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        # Send email with reset link
        messages.success(request, "Password reset link sent to your email.")
        return redirect('login')

    return render(request, 'account/forgot_password.html')

@login_required
def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')

        if new_password != new_password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'account/reset_password.html')

        user = request.user
        user.set_password(new_password)
        user.save()
        login(request, user)
        messages.success(request, "Password reset successfully!")
        return redirect('home')

    return render(request, 'account/reset_password.html')


@login_required
def deactivate_account(request):
    user = request.user
    if request.method == 'POST':
        user.is_active = False
        user.save()
        logout(request)
        messages.success(request, "Account deactivated successfully!")
        return redirect('home')

    return render(request, 'account/deactivate_account.html')


@login_required
@permission_required('account.can_view_student', raise_exception=True)
def view_students(request):
    students = Student.objects.all()
    return render(request, 'account/view.html', {'students': students})

@login_required
@permission_required('account.can_view_student', raise_exception=True)
def get_students(request):
    students = Student.objects.all()
    return render(request, 'account/students.html', {'students': students})

@login_required
@permission_required('account.can_view_student', raise_exception=True)
def get_student(request, student_id):
    student = Student.objects.get(id=student_id)
    return render(request, 'account/student.html', {'student': student})

@login_required
@permission_required('account.can_add_student', raise_exception=True)
def create_student(request):
    if request.method == 'POST':
        # Add student logic here
        return redirect('students')
    return render(request, 'account/add.html')

@login_required
@permission_required('account.can_change_student', raise_exception=True)
def update_student(request, student_id):
    student = Student.objects.get(id=student_id)
    if request.method == 'POST':
        # Update logic here
        return redirect('students')
    return render(request, 'account/edit.html', {'student': student})

@login_required
@permission_required('account.can_delete_student', raise_exception=True)
def delete_student(request, student_id):
    student = Student.objects.get(id=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('students')
    return render(request, 'account/delete.html', {'student': student})

@login_required
@permission_required('account.can_view_student', raise_exception=True)
def get_categories(request):
    return render(request, 'account/categories.html')


def get_settings(request):
    return render(request, 'account/settings.html')

def get_dropout_rate(request):
    summary = DropoutSummary.objects.first()
    total_students = summary.total_students
    total_dropouts = summary.total_dropouts
    dropout_rate = (total_dropouts / total_students) * 100 if total_students else 0
    return render(request, 'account/dropout_rate.html', {'dropout_rate': dropout_rate})

@login_required
def categorize_students(request):
    students = Student.objects.all()
    dropout_reasons = {
        "Academic": [],
        "Financial": [],
        "Health": [],
        "Personal": [],
        "Marriage": [],
        "Distance": [],
        "Death": [],
        "Other": []
    }

    for student in students:
        if student.dropout:
            dropout_reason = student.dropout_reason if student.dropout_reason else "Other"
            dropout_reasons[dropout_reason].append(student)

    return render(request, 'account/categorized_students.html', {'dropout_reasons': dropout_reasons})


@login_required
@permission_required('account.can_edit_student', raise_exception=True)
def edit_student(request, student_id):
    student = Student.objects.get(id=student_id)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        roll_no = request.POST.get('roll_no')
        department = request.POST.get('department')
        batch = request.POST.get('batch')
        section = request.POST.get('section')
        semester = request.POST.get('semester')
        cgpa = request.POST.get('cgpa')
        dropout = request.POST.get('dropout')
        dropout_reason = request.POST.get('dropout_reason')
        
        student.user.first_name = first_name
        student.user.last_name= last_name
        student.roll_no = roll_no
        student.department = department
        student.batch = batch
        student.section = section
        student.semester = semester
        student.cgpa = cgpa
        student.dropout = dropout
        student.dropout_reason = dropout_reason
        student.save()

        return redirect('students')
    return render(request, 'account/edit.html', {'student': student})


@login_required
@permission_required('account.can_add_student', raise_exception=True)
def create_student(request):
    # Retrieve all DropOut records to display in the form
    dropout_rsn_list = DropOut.objects.all()
    dropout_cases = DropOut._meta.get_field('DropOut_case').choices
    print(dropout_cases)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        roll_no = request.POST.get('roll_no')
        department = request.POST.get('department')
        batch = request.POST.get('batch')
        section = request.POST.get('section')
        semester = request.POST.get('semester')
        cgpa = request.POST.get('cgpa')
        dropout = request.POST.get('dropout')
        dropout_reason = request.POST.get('dropout_reason')

        # Create the student object
        student = Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            roll_no=roll_no,
            department=department,
            batch=batch,
            section=section,
            semester=semester,
            cgpa=cgpa,
            dropout=dropout,
            dropout_reason=dropout_reason
        )

        # If dropout is selected, link the student to the DropOut record
        if dropout and dropout_reason:
            dropout_instance = get_object_or_404(DropOut, id=dropout_reason)  # Assuming dropout_reason is the ID of DropOut
            dropout_instance.student = student  # Link the student to the DropOut
            dropout_instance.save()

        return redirect('students')

    return render(request, 'account/add.html', {'dropout_rsn_list': dropout_rsn_list,
        'dropout_cases': dropout_cases})
def custom_server_error_view(request):
    return render(request, '500.html', status=500)

def custom_method_not_allowed_view(request, exception): 
    return render(request, '405.html', status=405)

def custom_page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def custom_forbidden_view(request, exception): 
    return render(request, 'account/403.html', status=403)


def custom_permission_denied(request,exception):
    return render(request,'account/403.html', { 'error':"server is undermaintence. sorry for unconvinience"} ,status=403)


def dropout_summary(request):
    return render(request, 'account/dropout_summary.html')

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            wb = openpyxl.load_workbook(file)
            sheet = wb.active
            
            for row in sheet.iter_rows(min_row=2, values_only=True):  # Skip header row
                # Assuming the columns are in order: Username, Dropout Reason, Dropout Case
                username, reason, dropout_case = row
                
                try:
                    student = Student.objects.get(user__username=username)
                    DropOut.objects.create(
                        student=student,
                        reason=reason,
                        DropOut_case=dropout_case
                    )
                except Student.DoesNotExist:
                    # Handle case where student is not found
                    print(f"Student with username {username} does not exist.")
            
            return HttpResponse("Data uploaded successfully.")
    else:
        form = UploadFileForm()
    
    return render(request, 'account/upload.html', {'form': form})



def dropout_only(request):
    if request.method == 'POST':
        form = DropOutForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
        else:
            return render(request, 'account/dropout_only.html', {'form': form})

    form = DropOutForm()
    return render(request, 'account/dropout_only.html', {'form': form})
        
    
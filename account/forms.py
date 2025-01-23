import os
from django import forms
from .models import Student,DropOut,SchoolName,UserProfile
from django.core.validators import EmailValidator
from .validators import validate_phone_number
from PIL import Image
import io
from django.utils.timezone import now
from django.utils.timezone import datetime


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_no', 'batch', 'section', 'semester', 'dropout', 'dropout_reason']
        widgets = {
            'dropout': forms.RadioSelect(),
            'dropout_reason': forms.Textarea(attrs={'rows': 4, 'cols': 40,}),
            'batch':forms.RadioSelect(),
            'section':forms.RadioSelect(),
            'semester':forms.RadioSelect(),
            'role': forms.RadioSelect()

            }
        
        def clean_user(self):
            user = self.cleaned_data.get('user')
            if user:
                user_names = user.split(' ')

                first_name,last_name,middle_name = user_names
                if len(first_name)>1:
                    raise forms.ValidationError('First name should be only one word')
                if len(last_name)>1:
                    raise forms.ValidationError('Last name should be only one word')
                if len(middle_name):
                    raise forms.ValidationError('Middle name should be empty')
                
            else:
                raise forms.ValidationError('User name is required')
            return user
        



class UploadFileForm(forms.Form):
    file = forms.FileField()


class DropOutForm(forms.ModelForm):
    SEM = forms.ChoiceField(choices=DropOut.SEMESTER_CHOICE)
    dropout_choice = forms.ChoiceField(choices=DropOut.DROP_OUT_CHOICES)

    class Meta:  # Corrected 'meta' to 'Meta'
        model = DropOut
        fields = '__all__'
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 5:
            raise forms.ValidationError('name must be at least 5 characters long')
        
        if not name and not name[0].is_upper():
            raise forms.ValidationError('name must start with uppercase')
        
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_validator = EmailValidator()
        try:
            email_validator(email)
        except forms.ValidationError:
            raise forms.ValidationError('please enter valid email address')
        
        return email
    
    def clean_drop_out_reason(self):
        choice = self.cleaned_data.get('dropout_choice')
        valid_choices = [item[0] for item in DropOut.DROP_OUT_CHOICES]
        
        if choice not in valid_choices:
            raise forms.ValidationError('f{choice}invalid choice')
        
        if choice == 'other':
            reason = self.cleaned_data.get('dropout_choice')
            if not reason:
                raise forms.ValidationError('dropout reason is required')
            
            else:
                return reason
        return choice
    def clean_semester(self):
        semester = self.cleaned_data.get('semester')
        valid_sem_choice = [sem[0] for sem in DropOut.SEMESTER_CHOICE]
        if semester not in valid_sem_choice:
            raise forms.ValidationError('f{semester} is not valid')

        return semester


class SchoolNameForm(forms.ModelForm):
    logo = forms.ImageField()
    class Meta:
        model = SchoolName
        fields = '__all__'
        exclude = ['website']
        def clean_name(self):
            name = self.cleaned_data.get('name')
            if not name:
                raise forms.ValidationError('name is required')
            if not name[0].isupper():
                raise forms.ValidationError('name must start with uppercase')
            
            return name
    
        def clean_address(self):
            address = self.cleaned_data.get('address')
            if not address:
                raise forms.ValidationError('address is required')
            
            return address
    
        def clean_phone_number(self):
            phone_number = self.cleaned_data.get('phone_number')
            country_code = 'ETH'
            validate_phone_number(phone_number,country_code)


            return phone_number
    
        def clean_email(self):
            email = self.cleaned_data.get('email')
            try:
                EmailValidator(email)
            except forms.ValidationError:
                raise forms.ValidationError('invalid email')
        
            return email
    
        def logo_size(self):
            logo = self.cleaned_data.get('logo')
            if logo.size > 2 *1024*1024:
                raise forms.ValidationError('logo size must be less than 2MB')
            
            
            try:
                Image.open(logo).verify()

            except Exception:
                raise forms.ValidationError(_("Invalid Image"))
        
            width,height = logo.size
            if width != 300 and height != 400:
                raise forms.ValidationError('logo size must be 300 px width and 400 px width'
                                            )
            if width != height:
                raise forms.ValidationError('logo size must be square')
            
            return logo
    
        def clean_about(self):
            about = self.cleaned_data.get('about')
            if about is not type(str) or  about is not  type(int):
                raise forms.ValidationError('about must be string or integer')
            
            return about
    
        def clean_principal_role(self):
            principal = self.cleaned_data.get('principal')
            if self.request.user.is_authenticated:
                if not principal.role == 'principal':
                    raise forms.ValidationError('You do not have permission to select this principal.')
                else:
                    raise forms.ValidationError('please login as principal')
                
            return principal
    
        def clean_admin_role(self):
            admin = self.cleaned_data.get('admin')
            if self.request.user.is_authenticated:
                if not admin.role == 'admin' and not self.request.user.is_admin:
                    raise forms.ValidationError('You do not have permission to select this admin.')
                else:
                    raise forms.ValidationError('please login as admin')
            return admin
    
        def clean_staff_role(self):
            staff = self.cleaned_data.get('staff')
            if self.request.user.is_authenticated:
                if not staff.role == 'staff' and not self.request.user.is_staff:
                    raise forms.ValidationError('You do not have permission to select this staff.')
                else:
                    raise forms.ValidationError('please login as staff')
                
            return staff
        

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = '__all__'
        widgets = [
            forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),


        ]

        day = forms.IntegerField(min_value=1, max_value=31)
        month = forms.IntegerField(min_value=1, max_value=12)
        year = forms.IntegerField(min_value=1900, max_value=datetime.date)


        def clean_first_name(self):
            first_name = self.cleaned_data.get('first_name')
            if not first_name.isalpha():
                raise forms.ValidationError('First name should only contain letters')
            return first_name
        
        def clean_last_name(self):
            last_name = self.cleaned_data.get('last_name')
            if not last_name.isalpha():
                raise forms.ValidationError('Last name should only contain letters')
            return last_name
        
        def clean_image(self):
            image = self.cleaned_data.get('image')
            ext = os.path.splitext(image.name)[1].lower()
            allowed_formats = ['.png','jpeg','jpg']
            
            if image.size > 2 *  1024*1024:
                raise forms.ValidationError('Image size should be less than 2MB')
           
            width,height = image.size
            if width > 300 or height > 300:
                raise forms.ValidationError('Image should be less than 300x300')
            
        
            if ext not in allowed_formats:
                raise forms.ValidationError('Invalid image format. Allowed formats: JPG, JPEG, PNG, GIF.')
            try:
                Image.open(image).verify()
                
            except Exception as e:
                raise forms.ValidationError('Invalid Image')
            
        def clean_phone_number(self):
            phone_number = self.cleaned_data.get('phone_number')
            COUNTRY_CODE = 'ETH'
            validate_phone_number(phone_number,COUNTRY_CODE)
            return phone_number
        
        def clean_email(self):
            email = self.cleaned_data.get('email')
            validate_email = EmailValidator()
            try:
                validate_email(email)

            except forms.ValidationError as e:
                raise forms.ValidationError('Invalid email')
                
        def clean(self):
            cleaned_data = super().clean()
            day = cleaned_data.get('day')
            month = cleaned_data.get('month')
            year = cleaned_data.get('year')

            if day and month and year:
                
                try:
                    if month == 2:
                        if day > 29:
                            raise forms.ValidationError("February cannot have more than 29 days.")
                        if day == 29 and not self.is_leap_year(year):
                            raise forms.ValidationError("February has only 28 days in non-leap years.")
                    elif month in [4, 6, 9, 11]:  # April, June, September, November
                        if day > 30:
                            raise forms.ValidationError(f"The month {month} cannot have more than 30 days.")
                    else:  # January, March, May, July, August, October, December
                        if day > 31:
                            raise forms.ValidationError(f"The month {month} cannot have more than 31 days.")
                    
                    # Combine into a valid date for future checks
                    birth_day = datetime.date(year, month, day)
                    if birth_day > datetime.date.today():
                        raise forms.ValidationError("The birth date cannot be in the future.")

                except ValueError:
                    raise forms.ValidationError("Invalid date entered.")

                # Optionally store the combined date in cleaned_data
                cleaned_data['birth_day'] = birth_day

            return cleaned_data

        def is_leap_year(self, year):
            """Check if a year is a leap year."""
            return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

        def clean_sex(self):
            sex = self.cleaned_data.get('sex')
            if sex not in ['Male','Female']:
                raise forms.ValidationError('Invalid sex')
            return sex
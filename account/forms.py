from django import forms
from .models import Student,DropOut
from django.core.validators import EmailValidator

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_no', 'department', 'batch', 'section', 'semester', 'cgpa', 'dropout', 'dropout_reason']
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Student 
        fields = '__all__'


class UploadFileForm(forms.Form):
    file = forms.FileField()


class DropOutForm(forms.ModelForm):
    dropout_choice = forms.ChoiceField(choices=DropOut.DROP_OUT_CHOICES)
    class meta:
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
        reason = self.cleaned_data.get('drop_out_reason')

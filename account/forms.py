from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'roll_no', 'department', 'batch', 'section', 'semester', 'cgpa', 'dropout', 'dropout_reason']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Student 
        fields = '__all__'


class UploadFileForm(forms.Form):
    file = forms.FileField()

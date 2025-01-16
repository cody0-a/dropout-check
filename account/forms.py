from django import forms
from .models import Student

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

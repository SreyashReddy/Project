from django import forms
from .models import Task, StudentList


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields= ['title']


class StudentForm(forms.ModelForm):
    class Meta:
        model = StudentList
        fields = ['Register_Number','Name']

class UploadFileForm(forms.Form):
    file = forms.FileField()

# forms.py
from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone_number', 'address']

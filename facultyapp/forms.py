from django import forms
from .models import *


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = AddCourse
        fields = ['student', 'course', 'section']

class MarksForm(forms.ModelForm):
    class Meta:
        model = PostMarks
        fields = ['student', 'course', 'marks']
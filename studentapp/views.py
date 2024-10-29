from django.shortcuts import render

def StudentHomePage(request):
    return render(request,'studentapp/StudentHomePage.html')

from django.contrib.auth.models import User
from facultyapp.models import PostMarks  # Updated to use PostMarks
from adminapp.models import StudentList


def view_marks(request):
    user = request.user
    try:
        student_user = User.objects.get(username=user.username)
        student = StudentList.objects.get(Register_Number=student_user)
        marks = PostMarks.objects.filter(student=student)  # Changed to PostMarks
        return render(request, "studentapp/view_marks.html", {"marks": marks})
    except StudentList.DoesNotExist:
        return render(request, 'studentapp/no_student_record.html', {'error': 'No student record found'})

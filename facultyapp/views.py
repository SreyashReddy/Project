from django.contrib import messages  # Correct import for messages
from django.shortcuts import render, redirect
from .forms import AddCourseForm, MarksForm
from .models import AddCourse, PostMarks  # Correct import for Mark
from adminapp.models import StudentList

def FacultyHomePage(request):
    return render(request, 'facultyapp/FacultyHomePage.html')

def add_course(request):
    if request.method == 'POST':
        form = AddCourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facultyapp:view_student_list')  # Redirect to the view student list page
    else:
        form = AddCourseForm()

    return render(request, 'facultyapp/add_course.html', {'form': form})

def view_student_list(request):
    course = request.GET.get('course')
    section = request.GET.get('section')

    # Efficiently get students based on selected course and section
    student_courses = AddCourse.objects.all()

    # Filter student courses based on selected course and section
    if course:
        student_courses = student_courses.filter(course=course)
    if section:
        student_courses = student_courses.filter(section=section)

    # Fetch students who are in the filtered courses
    students = StudentList.objects.filter(id__in=student_courses.values('student_id')).distinct()

    # Choices for filtering
    course_choices = AddCourse.COURSE_CHOICES
    section_choices = AddCourse.SECTION_CHOICES

    context = {
        'students': students,
        'course_choices': course_choices,
        'section_choices': section_choices,
        'selected_course': course,
        'selected_section': section,
    }

    return render(request, 'facultyapp/view_student_list.html', context)

from django.core.mail import send_mail
from django.contrib.auth.models import User  # Assuming User is your custom user model
from .models import StudentList


def post_marks(request):
    if request.method == "POST":
        form = MarksForm(request.POST)
        if form.is_valid():
            marks_instance = form.save(commit=False)
            marks_instance.save()

            # Retrieve the User email based on the student in the form
            student = marks_instance.student
            student_user = student.user
            user_email = student_user.email

            subject = 'Marks Entered'
            message = f'Hello, {student_user.first_name}  marks for {marks_instance.course} have been entered. Marks: {marks_instance.marks}'
            from_email = 'funnybro0987@gmail.com'
            recipient_list = [user_email]
            send_mail(subject, message, from_email, recipient_list)

            return render(request, 'facultyapp/marks_success.html')
    else:
        form = MarksForm()
    return render(request, 'facultyapp/post_marks.html', {'form': form})
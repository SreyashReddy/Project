from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm, StudentForm, UploadFileForm
from .models import StudentList, Task
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import datetime
from datetime import timedelta
import calendar
import string
import random
from django.http import HttpResponse
# Project Home Page View
def projecthomepage(request):
    return render(request, 'adminapp/ProjectHomePage.html')


# Print Page Views
def printpagecall(request):
    return render(request, 'adminapp/printer.html')

def printpagelogic(request):
    user_input = None
    if request.method == "POST":
        user_input = request.POST.get('user_input', None)
        print(f'User input: {user_input}')
    return render(request, 'adminapp/printer.html', {'user_input': user_input})


# Exception Handling Views
def exceptionpagecall(request):
    return render(request, 'adminapp/ExceptionExample.html')

def exceptionpagelogic(request):
    if request.method == "POST":
        user_input = request.POST.get('user_input')
        result = None
        error_message = None
        try:
            num = int(user_input)
            result = 10 / num
        except Exception as e:
            error_message = str(e)
        return render(request, 'adminapp/ExceptionExample.html', {'result': result, 'error': error_message})
    return render(request, 'adminapp/ExceptionExample.html')


def randompagecall(request):
    return render(request, 'adminapp/randomExample.html')

def randomlogic(request):
    ran = ""

    if request.method == 'POST':
        number1 = int(request.POST.get('number1', 10))
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=number1))

    context = {'ran': ran}
    return render(request, 'adminapp/randomExample.html', context)

def calculatorpagecall(request):
    return render(request, 'adminapp/calculator.html')
def calculatorlogic(request):
    result = None

    if request.method == 'POST':
        num1 = float(request.POST.get('num1', 0))
        num2 = float(request.POST.get('num2', 0))
        operation = request.POST.get('operation')

        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            if num2 != 0:
                result = num1 / num2
            else:
                result = 'Cannot divide by zero'

    context = {'result': result}
    return render(request, 'adminapp/calculator.html', context)


# User Registration Views
def UserRegistercall(request):
    return render(request, 'adminapp/UserRegisterPage.html')

def UserRegisterlogic(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('password1')

        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'OOPS! Username already taken.')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'OOPS! Email already registered.')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=pass1,
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )
                user.save()
                messages.success(request, 'Account created successfully!')
                return redirect('projecthomepage')
        else:
            messages.info(request, 'Passwords do not match.')
    return render(request, 'adminapp/UserRegisterPage.html')


# User Login and Logout Views
def UserLoginPageCall(request):
    return render(request, 'adminapp/UserLoginPage.html')

def UserLoginLogic(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if len(username) == 10:
                messages.success(request, 'Login successful as student!')
                return redirect('studentapp:StudentHomePage')
            elif len(username) == 4:
                messages.success(request, 'Login successful as faculty!')
                return redirect('facultyapp:home')
            else:
                messages.error(request, 'Username length does not match student or faculty criteria.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'adminapp/UserLoginPage.html')

def logout_view(request):
    logout(request)
    return redirect('projecthomepage')


# Task Management Views
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_task')
    else:
        form = TaskForm()
    tasks = Task.objects.all()
    return render(request, 'adminapp/add_task.html', {'form': form, 'tasks': tasks})

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('add_task')


# Student Management Views
# def add_student(request):
#     if request.method == 'POST':
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('student_list')
#     else:
#         form = StudentForm()
#     return render(request, 'adminapp/add_student.html', {'form': form})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            register_number = form.cleaned_data['Register_Number']
            try:
                user = User.objects.get(username=register_number)
                student.user = user  # Assign the matching User to the student
            except User.DoesNotExist:
                form.add_error('Register_Number', 'No user found with this Register Number')
                return render(request, 'adminapp/add_student.html', {'form': form})
            student.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'adminapp/add_student.html', {'form': form})
def student_list(request):
    students = StudentList.objects.all()
    return render(request, 'adminapp/student_list.html', {'students': students})


# File Upload and Chart Generation Views
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid() and 'file' in request.FILES:
            file = request.FILES['file']
            try:
                df = pd.read_csv(file, parse_dates=['Date'], dayfirst=True)
            except Exception as e:
                return render(request, 'adminapp/Chart.html', {'form': form, 'error': f"Error reading CSV: {str(e)}"})

            total_sales = df['Sales'].sum()
            average_sales = df['Sales'].mean()

            df['Month'] = df['Date'].dt.month
            monthly_sales = df.groupby('Month')['Sales'].sum()
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            monthly_sales.index = monthly_sales.index.map(lambda x: month_names[x - 1])

            plt.figure(figsize=(6, 6))
            plt.pie(monthly_sales, labels=monthly_sales.index, autopct='%1.1f%%')
            plt.title('Sales Distribution per Month')

            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            plt.close()

            return render(request, 'adminapp/Chart.html', {
                'form': form,
                'total_sales': total_sales,
                'average_sales': average_sales,
                'chart': image_data
            })
    else:
        form = UploadFileForm()
    return render(request, 'adminapp/Chart.html', {'form': form})


# Date and Time Views
def datetimepagecall(request):
    return render(request, 'adminapp/datetimepage.html')

def datetimepagelogic(request):
    if request.method == "POST":
        number1 = int(request.POST.get('date1'))
        current_date = datetime.datetime.now()
        future_date = current_date + timedelta(days=number1)
        year = future_date.year
        is_leap_year = "Leap year" if calendar.isleap(year) else "Not leap year"

        context = {
            'future_date': future_date,
            'is_leap_year': is_leap_year,
            'year': year,
            'number1': number1
        }
        return render(request, 'adminapp/datetimepage.html', context)
    return render(request, 'adminapp/datetimepage.html')

def feedbackpagecall(request):
    return render(request, 'adminapp/feedback.html')


from django.http import HttpResponse
from django.shortcuts import render
from .models import Student

def feedbacklogic(request):
    if request.method == 'POST':
        # Get data from the form
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        description = request.POST.get('description')
        text_field = request.POST.get('textfield')

        # Create a new Student object and save the data to the database
        student = Student(
            username=username,
            email=email,
            phone=phone,
            description=description,
            textfield=text_field
        )
        student.save()

        # Provide feedback or redirect
        return HttpResponse(f"Form submitted! Username: {username}, Email: {email}")

    # If it's a GET request, render the form
    return render(request, 'adminapp/feedback.html')


# views.py
from django.shortcuts import render
from .forms import ContactForm

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact
from .forms import ContactForm


def contact_manager(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('contact_list')  # Redirect back to the contact list

    contacts = Contact.objects.all()
    return render(request, 'adminapp/contact_list.html', {'form': form, 'contacts': contacts})


def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    return redirect('contact_list')


from django.urls import path, include
from . import views

urlpatterns =[
    path('',views.projecthomepage,name='projecthomepage'),
    path('printpagecall/',views.printpagecall,name='printpagecall'),
    path('printpagelogic/',views.printpagelogic,name='printpagelogic'),
    path('exceptionpagecall',views.exceptionpagecall,name='exceptionpagecall'),
    path('exceptionpagelogic',views.exceptionpagelogic,name='exceptionpagelogic'),
    path('calculatorpagecall/',views.calculatorpagecall, name='calculatorpagecall'),
    path('calculatorlogic/', views.calculatorlogic, name='calculatorlogic'),
    path('randompagecall/',views.randompagecall, name='randompagecall'),
    path('randomlogic/', views.randomlogic, name='randomlogic'),
    path('UserRegistercall',views.UserRegistercall,name='UserRegistercall'),
    path('UserRegisterlogic',views.UserRegisterlogic,name='UserRegisterlogic'),
    path('add_task/', views.add_task, name='add_task'),
    path('<int:pk>/delete/', views.delete_task, name='delete_task'),
    path('UserLoginPageCall',views.UserLoginPageCall,name='UserLoginPageCall'),
    path('UserLoginLogic',views.UserLoginLogic,name='UserLoginLogic'),
    path('logout/', views.logout_view, name='logout'),
    path('add_student',views.add_student,name='add_student'),
    path('student_list',views.student_list,name='student_list'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('datetimepagelogic/', views.datetimepagelogic, name='datetimepagelogic'),
    path('datetimepagecall/', views.datetimepagecall, name='datetimepagecall'),
    path('feedbackpagecall/',views.feedbackpagecall, name='feedbackpagecall'),
    path('feedbacklogic/', views.feedbacklogic, name='feedbacklogic'),
    path('contacts/', views.contact_manager, name='contact_list'),
    path('delete_contact/<int:pk>/', views.delete_contact, name='delete_contact'),

]
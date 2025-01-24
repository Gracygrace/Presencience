from django.contrib import admin
from django.urls import path
from home.views import home,register_teacher,login_teacher,logout_teacher,capture_attendance,create_class,list_classes,delete_class,add_student,list_students,delete_student,attendance_report,individual_student_report,class_details

urlpatterns = [
    
    path('', home, name='home'),
    path('register/', register_teacher, name='register'),
    path('login/', login_teacher, name='login'),
    path('logout/', logout_teacher, name='logout'),

     # Class Management
    path("class/<int:class_id>/", class_details, name="class_details"),
    path('class/create/', create_class, name='create_class'),
    path('class/list/', list_classes, name='list_classes'),
    path('class/delete/<int:class_id>/', delete_class, name='delete_class'),

    # Student Management
    path('student/add/<int:class_id>/', add_student, name='add_student'),
    path('student/list/<int:class_id>/', list_students, name='list_students'),
    path('student/delete/<int:student_id>/', delete_student, name='delete_student'),

    # Attendance
    path('attendance/capture/<int:class_id>/', capture_attendance, name='capture_attendance'),
    path('attendance/report/<int:class_id>/', attendance_report, name='attendance_report'),
    path('student/report/<int:student_id>/', individual_student_report, name='individual_student_report'),
]


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:  # Only for development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

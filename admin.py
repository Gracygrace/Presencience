from django.contrib import admin
from home.models import Class,Attendance,Student

# Register your models here.

admin.site.register(Class)
admin.site.register(Attendance)
admin.site.register(Student)
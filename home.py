from django.shortcuts import render
from django.http import HttpResponse
from home.models import Class,Attendance,Student
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import face_recognition
from django.shortcuts import render, get_object_or_404, redirect



def home(request):
    if not request.user.is_authenticated:
        # Render a home page for unauthenticated users
        return render(request, 'home.html', {'classes': None})

    # Render a home page with class information for authenticated users
    classes = Class.objects.filter(teacher=request.user)
    return render(request, 'home.html', {'classes': classes})

@login_required
def class_details(request, class_id):
    class_obj = Class.objects.get(id=class_id, teacher=request.user)
    students = class_obj.students.all()
    return render(request, "class_details.html", {"class_obj": class_obj, "students": students})

@login_required
def create_class(request):
    if request.method == "POST":
        name = request.POST.get("name")
        Class.objects.create(name=name, teacher=request.user)
        return redirect("home")
    return render(request, "create_class.html")

@login_required
def list_classes(request):
    classes = Class.objects.filter(teacher=request.user)
    return render(request, "list_classes.html", {"classes": classes})

@login_required
def delete_class(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id, teacher=request.user)
    if request.method == "POST":
        class_obj.delete()
        return redirect("home")
    return render(request, "delete_class.html", {"class_obj": class_obj})


@login_required
def add_student(request, class_id):
    class_obj = Class.objects.get(id=class_id, teacher=request.user)
    if request.method == "POST":
        name = request.POST.get("name")
        photo = request.FILES.get("photo")
        Student.objects.create(name=name, class_name=class_obj, photo=photo)
        return redirect("class_details", class_id=class_id)
    return render(request, "add_student.html", {"class_obj": class_obj})

@login_required
def list_students(request, class_id):
    class_obj = Class.objects.get(id=class_id, teacher=request.user)
    students = class_obj.students.all()
    return render(request, "list_students.html", {"class_obj": class_obj, "students": students})

@login_required
def delete_student(request, student_id):
    student = Student.objects.get(id=student_id)
    if student.class_name.teacher == request.user:
        student.delete()
        return redirect("list_classes")
    return render(request, "delete_students.html", {"students": student})


def capture_attendance(request, class_id):
    class_obj = Class.objects.get(id=class_id, teacher=request.user)  # Fetch class_obj
    if request.method == "POST":
        uploaded_photo = request.FILES.get("class_photo")
        known_faces = []
        student_map = {}

        for student in class_obj.students.all():
            student_image = face_recognition.load_image_file(student.photo.path)
            encoding = face_recognition.face_encodings(student_image)[0]
            known_faces.append(encoding)
            student_map[tuple(encoding)] = student

        class_image = face_recognition.load_image_file(uploaded_photo)
        class_faces = face_recognition.face_encodings(class_image)

        for face_encoding in class_faces:
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            if True in matches:
                match_index = matches.index(True)
                student = student_map[tuple(known_faces[match_index])]
                Attendance.objects.create(student=student, is_present=True)

        return redirect("attendance_report", class_id=class_id)
    return render(request, "capture_attendance.html", {"class_obj": class_obj})  # Pass `class_obj`

@login_required
def attendance_report(request, class_id):
    class_obj = Class.objects.get(id=class_id, teacher=request.user)
    students = class_obj.students.all()
    attendance_data = {
        student: student.attendance_records.all()
        for student in students
    }
    return render(request, "attendance_report.html", {"class_obj": class_obj, "attendance_data": attendance_data})

@login_required
def individual_student_report(request, student_id):
    student = Student.objects.get(id=student_id)
    records = student.attendance_records.all()
    return render(request, "student_report.html", {"student": student, "records": records})

from PIL import Image

def validate_image(photo):
    try:
        img = Image.open(photo)
        img.verify()
        return True
    except (IOError, SyntaxError):
        return False

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def register_teacher(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        User.objects.create_user(username=username, password=password)
        return redirect("login")
    return render(request, "register_teacher.html")

def login_teacher(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
    return render(request, "login.html")

@login_required
def logout_teacher(request):
    logout(request)
    return redirect("home")

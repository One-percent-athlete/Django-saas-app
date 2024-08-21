from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.shortcuts import render, redirect

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        if all([username, password]):
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home_view')
    return render(request, "auth/login.html", {})

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")
        username_exists = User.objects.filter(username__iexact=username).exists()
        email_exists = User.objects.filter(email__iexact=email).exists()
        if username_exists or email_exists:
            if password == password1:
                User.objects.create_user(username=username, email=email, password=password)
                return redirect('home_view')
            return redirect('register_view')
        return redirect('register_view')
    return render(request, "auth/register.html", {})
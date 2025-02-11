from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def login_view(request):
    """Display the login page and authenticate user."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, '../templates/login.html')

@login_required
def home_view(request):
    """Display a simple home page for authenticated users."""
    return render(request, '../templates/home.html')


def logout_view(request):
    """Log out the user."""
    logout(request)
    return redirect('login')

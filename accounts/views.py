from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login Successfully")
            return redirect('dashboard') 
        else:
            # Return an 'invalid login' error message.
            messages.success(request, "Invalid username or password")
            return render(request, 'accounts/login.html',
            {'error': 'Invalid username or password'
            })
    else:
        return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    
    messages.success(request, "Logout Successfully")
    return redirect('login')

def home(request):
    return redirect('dashboard')  # Redirect to the dashboard view after login
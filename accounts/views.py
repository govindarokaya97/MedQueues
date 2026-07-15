from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages


def login_view(request):
    if request.user.is_authenticated:
        if request.user.force_password_change:
            return redirect("force_password_change")

        if request.user.role == "admin":
            return redirect("dashboard")
        elif request.user.role == "doctor":
            return redirect("doctor_dashboard")
        elif request.user.role == "patient":
            return redirect("patient_dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password.")
            return render(request, "accounts/login.html")

        login(request, user)

        if user.force_password_change:
            return redirect("force_password_change")

        if user.role == "admin":
            return redirect("dashboard")
        elif user.role == "doctor":
            return redirect("doctor_dashboard")
        elif user.role == "patient":
            return redirect("patient_dashboard")

        messages.error(request, "Unknown user role.")
        return redirect("login")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")


@login_required
def force_password_change_view(request):
    if not request.user.force_password_change:
        if request.user.role == "admin":
            return redirect("dashboard")
        elif request.user.role == "doctor":
            return redirect("doctor_dashboard")
        elif request.user.role == "patient":
            return redirect("patient_dashboard")

    if request.method == "POST":
        form = SetPasswordForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            user.force_password_change = False
            user.save()

            update_session_auth_hash(request, user)

            messages.success(request, "Password changed successfully.")

            if user.role == "admin":
                return redirect("dashboard")
            elif user.role == "doctor":
                return redirect("doctor_dashboard")
            elif user.role == "patient":
                return redirect("patient_dashboard")

    else:
        form = SetPasswordForm(request.user)

    return render(request, "accounts/force_password_change.html", {"form": form})
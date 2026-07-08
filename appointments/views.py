from django.shortcuts import render, redirect
from .models import Appointment
from .forms import AppointmentForm
from django.contrib import messages

# Create your views here.

def appointment_list(request):
    appointments = Appointment.objects.select_related(
        "patient",
        "doctor",
        "doctor__user",
    )

    return render(
        request, 
        "appointments/appointments_list.html",
        {"appointments":appointments}
    )

def appointment_create(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Appointment Booked Successfully")
            return redirect("appointments_list")
    
    else:
        form = AppointmentForm()
    
    return render(
        request, 
        "appointments/appointments_form.html",
        {"form":form}
    )
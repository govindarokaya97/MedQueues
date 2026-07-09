from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Appointment
from .forms import AppointmentForm
from django.contrib import messages
from datetime import date



# Create your views here.

def appointment_list(request):
    appointments = Appointment.objects.select_related(
        "patient",
        "doctor",
        "doctor__user",
    )

    search = request.GET.get("search")
    status = request.GET.get("status")
    date = request.GET.get("date")

    if search:
        appointments = appointments.filter(
            Q(patient__first_name__icontans=search) |
            Q(patient__last_name__icontans=search) |
            Q(doctor__user__first_name__icontans=search) |
            Q(doctor__user__last_name__icontans=search)    
        )
    if status:
        appointments = appointments.filter(status=status)
    
    if date:
        appointments = appointments.filter(appointment_date=date)
        

    return render(
        request, 
        "appointments/appointments_list.html",
        {
            "appointments":appointments,
            "status_choices": Appointment.STATUS_CHOICES
        }
    )

def appointment_create(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Appointment Booked Successfully")
            return redirect("appointments_list")
        
        doctor = form.cleaned_data["doctor"]

        if not doctor.available:
            form.add_error(
                "doctor",
                "This doctor is currently unavailable."
            )
    
    else:
        form = AppointmentForm()
    
    return render(
        request, 
        "appointments/appointments_form.html",
        {"form":form}
    )

def appointment_detail(request, id):
    appointment = get_object_or_404(Appointment, id=id)

    return render(request,"appointments/appointments_detail.html",{
        "appointment":appointment
    })


def appointment_update(request, id):
    appointment = get_object_or_404(Appointment, id=id)

    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)

        if form.is_valid():
            form.save()
            messages.success(request, "Edited Booked Appointment")
            return redirect("appointments_list")
    
    else:
        form = AppointmentForm(instance=appointment)
    
    return render(
        request, 
        "appointments/appointments_form.html",
        {"form":form}
    )


def appointment_delete(request, id):
    appointment = get_object_or_404(Appointment, id=id)

    if request.method == "POST":
        appointment.delete()
        messages.success(request, "Removed Booked Appointment")
        return redirect("appointments_list")
    
    return render(request,"appointments/appointments_confirm_delete.html",{
        "appointment":appointment
    })


def appointment_dashboard(request):
    today = date.today()

    appointments_today = Appointment.objects.filter(
        appointment_date=today
    )

    context = {
        "appointments_today": appointments_today.count(),
        "pending": appointments_today.filter(
            status="Pending"
        ).count(),
        "confirmed": appointments_today.filter(
            status="Confirmed"
        ).count(),
        "completed": appointments_today.filter(
            status="Completed"
        ).count(),
    }

    return render(request, "appointments/appointments_dashboard.html", context)
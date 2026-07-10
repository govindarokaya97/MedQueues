from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Appointment
from .forms import AppointmentForm
from django.contrib import messages
from datetime import date
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth.decorators import login_required



# Create your views here.

@login_required
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
            Q(patient__first_name__icontains=search) |
            Q(patient__last_name__icontains=search) |
            Q(doctor__user__first_name__icontains=search) |
            Q(doctor__user__last_name__icontains=search)    
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


@login_required
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


@login_required
def appointment_detail(request, id):
    appointment = get_object_or_404(Appointment, id=id)

    return render(request,"appointments/appointments_detail.html",{
        "appointment":appointment
    })


@login_required
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


@login_required
def appointment_delete(request, id):
    appointment = get_object_or_404(Appointment, id=id)

    if request.method == "POST":
        appointment.delete()
        messages.success(request, "Removed Booked Appointment")
        return redirect("appointments_list")
    
    return render(request,"appointments/appointments_confirm_delete.html",{
        "appointment":appointment
    })


@login_required
def appointment_dashboard(request):
    today = date.today()

    appointments_today = Appointment.objects.filter(appointment_date=today)
    # appointments_today = Appointment.objects.all()


    context = {
        "appointments_today": appointments_today.count(),
        "pending": appointments_today.filter(status="Pending").count(),
        "confirmed": appointments_today.filter(status="Confirmed").count(),
        "completed": appointments_today.filter(status="Completed").count(),
    }

    return render(request, "appointments/appointments_dashboard.html", context)


@login_required
def upcoming_appointments(request):
    appointments = Appointment.objects.filter(
        appointment_date__gte=timezone.now().date()
    )

    context = {
        "appointments": appointments
    }

    return render(request, "appointments/upcoming.html", context)


@login_required
def appointment_report(request):
    report = (
        Appointment.objects.values("status")
        .annotate(total=Count("id"))
    )

    context = {
        "report": report
    }

    return render(request, "appointments/report.html", context)

def appointment_slip(request, id):
    appointment = get_object_or_404(Appointment, id=id)

    return render(request, "appointments/appointments_slip.html", {
        "appointment": appointment
    })

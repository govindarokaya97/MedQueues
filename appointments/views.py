from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Appointment
from .forms import AppointmentForm
from django.contrib import messages
from datetime import date
from django.utils import timezone
from django.db.models import Count
from accounts.decorators import role_required



# Create your views here.

@role_required("admin", "doctor")
def appointment_list(request):
    appointments = Appointment.objects.select_related(
        "patient__user",
        "doctor__user",
    ).all()
    paginate_by = 10

    search = request.GET.get("search")
    status = request.GET.get("status")
    date = request.GET.get("date")

    if search:
        appointments = appointments.filter(
            Q(patient__user__first_name__icontains=search) |
            Q(patient__user__last_name__icontains=search) |
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


@role_required("admin", "doctor", "patient")
def appointment_create(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if request.user.role == "patient":
            form.fields.pop("patient", None)

        if form.is_valid():
            appointment = form.save(commit=False)

            if request.user.role == "patient":
                appointment.patient = request.user.patient

            appointment.save()

            messages.success(request, "Appointment Booked Successfully")
            return redirect("appointments_list")

    
    else:
        form = AppointmentForm()

        if request.user.role == "patient":
            form.fields.pop("patient", None)

    return render(
        request, 
        "appointments/appointments_form.html",
        {"form":form}
    )


@role_required("admin", "doctor", "patient")
def appointment_detail(request, id):
    appointment = get_object_or_404(Appointment, id=id)

    return render(request,"appointments/appointments_detail.html",{
        "appointment":appointment
    })


@role_required("admin", "doctor")
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


@role_required("admin")
def appointment_delete(request, id):
    appointment = get_object_or_404(Appointment, id=id)

    if request.method == "POST":
        appointment.delete()
        messages.success(request, "Removed Booked Appointment")
        return redirect("appointments_list")
    
    return render(request,"appointments/appointments_confirm_delete.html",{
        "appointment":appointment
    })


@role_required("admin", "doctor")
def appointment_dashboard(request):
    today = date.today()
    appointments_today = Appointment.objects.filter(
        appointment_date=today
    )



    context = {
        "total_appointments": appointments_today.count(),
        "pending": appointments_today.filter(status="Pending").count(),
        "confirmed": appointments_today.filter(status="Confirmed").count(),
        "completed": appointments_today.filter(status="Completed").count(),
        "cancelled": appointments_today.filter(status="Cancelled").count(),

    }

    return render(request, "appointments/appointments_dashboard.html", context)


@role_required("admin", "doctor")
def upcoming_appointments(request):
    appointments = Appointment.objects.select_related(
        "patient__user",
        "doctor__user",
    ).filter(
        appointment_date__gte=timezone.now().date()
    )

    context = {
        "appointments": appointments
    }

    return render(request, "appointments/upcoming.html", context)


@role_required("admin")
def appointment_report(request):
    report = (
        Appointment.objects.values("status")
        .annotate(total=Count("id"))
    )

    context = {
        "report": report
    }

    return render(request, "appointments/report.html", context)

@role_required("admin", "doctor", "patient")
def appointment_slip(request, id):
    appointment = get_object_or_404(Appointment, id=id)

    return render(request, "appointments/appointments_slip.html", {
        "appointment": appointment
    })
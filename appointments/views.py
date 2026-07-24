from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Appointment
from .forms import AppointmentForm
from django.contrib import messages
from datetime import date
from django.utils import timezone
from django.db.models import Count
from django.http import Http404, HttpResponseForbidden, JsonResponse
from doctors.models import Doctor
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
            if request.user.role in ("admin", "doctor"):
                return redirect("appointments_list")
            return redirect("appointments_detail", id=appointment.id)

    
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
    if request.user.role == "patient" and appointment.patient.user_id != request.user.id:
        raise Http404
    
    try:
        lab_requests = appointment.labrequest
    except:
        lab_requests = None

    return render(request,"appointments/appointments_detail.html",{
        "appointment":appointment,
        "lab_requests" : lab_requests
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
    if request.user.role == "patient" and appointment.patient.user_id != request.user.id:
        raise Http404

    return render(request, "appointments/appointments_slip.html", {
        "appointment": appointment
    })


# ---------------------------------------------------------------------
# Live queue / token system
# ---------------------------------------------------------------------

@role_required("admin", "doctor")
def appointment_check_in(request, id):
    """Front-desk / doctor checks a patient in and issues them a queue token."""
    appointment = get_object_or_404(Appointment, id=id)

    if request.method == "POST":
        if appointment.status in ("Cancelled", "Completed"):
            messages.error(request, "Cannot check in a cancelled or completed appointment.")
        elif appointment.queue_number is not None:
            messages.info(request, f"Already checked in with token #{appointment.queue_number}.")
        else:
            appointment.check_in()
            messages.success(request, f"Checked in. Token number: {appointment.queue_number}")

    return redirect("appointments_detail", id=appointment.id)


@role_required("admin", "doctor")
def call_next_patient(request, doctor_id):
    """Doctor calls the next waiting token: finishes the current one (if any)
    and moves the lowest-numbered waiting patient into 'In Progress'."""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.user.role == "doctor" and doctor.user_id != request.user.id:
        return HttpResponseForbidden("You can only manage your own queue.")
    today = timezone.now().date()

    if request.method == "POST":
        current = Appointment.objects.filter(
            doctor=doctor, appointment_date=today, status="In Progress"
        ).first()
        if current:
            current.status = "Completed"
            current.save(update_fields=["status"])

        next_up = (
            Appointment.objects.filter(
                doctor=doctor, appointment_date=today, status="Waiting"
            )
            .order_by("queue_number")
            .first()
        )
        if next_up:
            next_up.status = "In Progress"
            next_up.save(update_fields=["status"])
            messages.success(request, f"Now serving token #{next_up.queue_number}.")
        else:
            messages.info(request, "No patients waiting in the queue.")

    return redirect("queue_board", doctor_id=doctor.id)


@role_required("admin", "doctor", "patient")
def queue_board(request, doctor_id):
    """Waiting-room display: who's being served now and who's next."""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.user.role == "doctor" and doctor.user_id != request.user.id:
        return HttpResponseForbidden("You can only view your own queue.")
    today = timezone.now().date()

    now_serving = Appointment.objects.filter(
        doctor=doctor, appointment_date=today, status="In Progress"
    ).first()

    waiting = Appointment.objects.select_related("patient__user").filter(
        doctor=doctor, appointment_date=today, status="Waiting"
    ).order_by("queue_number")

    return render(request, "appointments/queue_board.html", {
        "doctor": doctor,
        "now_serving": now_serving,
        "waiting": waiting,
    })


@role_required("admin", "doctor", "patient")
def queue_board_data(request, doctor_id):
    """JSON snapshot of the queue for lightweight polling (no page reload)."""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.user.role == "doctor" and doctor.user_id != request.user.id:
        return HttpResponseForbidden("You can only view your own queue.")
    today = timezone.now().date()

    now_serving = Appointment.objects.filter(
        doctor=doctor, appointment_date=today, status="In Progress"
    ).first()

    waiting = Appointment.objects.filter(
        doctor=doctor, appointment_date=today, status="Waiting"
    ).order_by("queue_number").values_list("queue_number", flat=True)

    return JsonResponse({
        "now_serving": now_serving.queue_number if now_serving else None,
        "waiting_tokens": list(waiting),
        "waiting_count": len(waiting),
    })


@role_required("patient")
def my_queue_status(request):
    """A patient's own live token status for today, across all their appointments."""
    today = timezone.now().date()
    appointments = Appointment.objects.select_related("doctor__user").filter(
        patient=request.user.patient,
        appointment_date=today,
    ).exclude(status__in=["Cancelled", "Completed"])

    return render(request, "appointments/my_queue_status.html", {
        "appointments": appointments,
    })

from django.shortcuts import render
from accounts.decorators import role_required
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
from django.utils import timezone


@role_required("admin")
def dashboard_view(request):
    today = timezone.now().date()

    today_count = Appointment.objects.filter(appointment_date=today).count()
    pending = Appointment.objects.filter(status="Pending").count()
    completed = Appointment.objects.filter(status="Completed").count()
    latest_doctors = Doctor.objects.order_by("-id")[:5]
    latest_patients = Patient.objects.order_by("-id")[:5]
    
    context = {
        "user": request.user,
        "doctor_count": Doctor.objects.count(),
        "patient_count": Patient.objects.count(),
        "appointment_count": Appointment.objects.count(),
        "latest_doctors": latest_doctors,
        "latest_patients": latest_patients,
        "today": today_count,
        "pending": pending,
        "completed": completed,

        "today_count": today_count,
        "today_date": today,
    }

    return render(request, 'dashboard/dashboard.html', context)
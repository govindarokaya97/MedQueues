from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment


@login_required
def dashboard_view(request):
    latest_doctors = Doctor.objects.order_by("-id")[:5]
    latest_patients = Patient.objects.order_by("-id")[:5]
    context = {
        "doctor_count" : Doctor.objects.count(),
        "patient_count" : Patient.objects.count(),
        "appointment_count" : Appointment.objects.count(),
        "latest_doctors" : latest_doctors, 
        "latest_patients" : latest_patients,
    }

    return render(request, 'dashboard/index.html', context)
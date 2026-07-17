from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Patient
from django.contrib import messages 
from django.utils import timezone 
from appointments.models import Appointment
from .forms import PatientForm, PatientUserForm
from accounts.models import CustomUser
from accounts.utils import generate_username
from accounts.decorators import role_required
from django.utils.crypto import get_random_string
from laboratory.models import LabRequest



# Create your views here.
@role_required("admin","doctor")
def patient_list(request):
    search = request.GET.get('search')
    gender = request.GET.get('gender')

    patients = Patient.objects.select_related("user").all()

    if search:
        patients = patients.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(phone__icontains=search)
        )
    
    if gender:
        patients = patients.filter(gender=gender)

    return render(request, 'patients/patient_list.html', {
        'patients': patients,
        'search': search or '',
        'gender_male': gender == 'Male',
        'gender_female': gender == 'Female',
        'gender_other': gender == 'Other',
        })


@role_required("admin")
def patient_create(request):

    password = get_random_string(10)

    if request.method == "POST":
        user_form = PatientUserForm(request.POST)
        patient_form = PatientForm(request.POST, request.FILES)

        if user_form.is_valid() and patient_form.is_valid():
            password = get_random_string(10)
            username = generate_username("PT")

            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                role="patient",
                first_name=user_form.cleaned_data["first_name"],
                last_name=user_form.cleaned_data["last_name"],
                email=user_form.cleaned_data["email"],
            )

            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save()

            messages.success(
                request,
                f"Patient account created successfully.\n"
                f"Username: {username}\n"
                f"Temporary Password: {password}"
            )

            return redirect("patient_list")
    else:
        user_form = PatientUserForm()
        patient_form = PatientForm()

    return render(request, "patients/patient_form.html", {
        "user_form": user_form,
        "patient_form": patient_form,
    })


@role_required("admin","doctor")
def patient_detail(request, id):
    patient = get_object_or_404(Patient, id=id)
    lab_requests = LabRequest.objects.filter(patient=patient)
    
    return render(request, 'patients/patient_detail.html', {
        'patient': patient,
        'lab_requests':lab_requests
        })


@role_required("patient")
def patient_dashboard(request):
    patient = get_object_or_404(
        Patient,
        user=request.user
    )

    recent_appointments = Appointment.objects.filter(
        patient=patient
    ).order_by("-appointment_date", "-appointment_time")[:5]

    upcoming_appointments = Appointment.objects.filter(
        patient=patient,
        appointment_date__gte=timezone.now().date()
    ).count()

    context = {
        "patient": patient,
        "recent_appointments": recent_appointments,
        "upcoming_appointments": upcoming_appointments,
    }

    return render(request, "patients/patient_dashboard.html", context)


@role_required("admin")
def patient_update(request, id):
    patient = get_object_or_404(Patient, id=id)

    if request.method == 'POST':
        form = PatientForm(
            request.POST,
            request.FILES,
            instance=patient)

        if form.is_valid():
            form.save()
            messages.success(request, "Patient updated successfully")
            return redirect('patient_list')

    else:
        form = PatientForm(instance=patient)

    return render(request, 'patients/patient_update.html', {
        'form': form
    })


@role_required("admin")
def patient_delete(request, id):
    patient = get_object_or_404(Patient, id=id)

    if request.method == 'POST':
        user = patient.user
        patient.delete()
        user.delete()
        messages.success(request, "Patient deleted successfully")
        return redirect('patient_list')
        
    return render(request, 'patients/patient_confirm_delete.html', {
        'patient': patient
        })



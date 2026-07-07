from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient
from .forms import PatientForm

# Create your views here.

def patient_list(request):
    search = request.GET.get('search')

    patients = Patient.objects.all()

    if search:
        patients =(
            patients.filter(first_name__icontains=search) |
            patients.filter(last_name__icontains=search) | 
            patients.filter(phone__icontains=search)
        )
    return render(request, 'patients/patient_list.html', {
        'patients': patients,
        'search': search
        })


def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'patients/patient_form.html', {
        'form': form
        })

def patient_detail(request, id):
    patient = get_object_or_404(Patient, id=id)
    return render(request, 'patients/patient_detail.html', {
        'patient': patient
        })

def patient_update(request, id):
    patient = get_object_or_404(Patient, id=id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/patient_form.html', {
        'form': form
        })

def patient_delete(request, id):
    patient = get_object_or_404(Patient, id=id)

    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')
        
    return render(request, 'patients/patient_confirm_delete.html', {
        'patient': patient
        })
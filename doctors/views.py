from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import DoctorForm, DoctorUserForm
from .models import Doctor, Department


# Create your views here.

def doctor_list(request):
    doctors = Doctor.objects.select_related("user","department")

    search = request.GET.get("search")
    department = request.GET.get("department")

    if search:
        doctors = doctors.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(specialization__icontains=search)
        )
    if department:
        doctors = doctors.filter(department_id=department)

    departments = Department.objects.all()

    context={
        "doctors": doctors,
        "departments": departments,
    }
    return render(request, "doctors/doctor_list.html", context)


def doctor_create(request):
    if request.method == "POST":
        # print("POST request received")
        user_form = DoctorUserForm(request.POST)
        doctor_form = DoctorForm(request.POST, request.FILES)

        # print(user_form.is_valid())
        # print(user_form.is_valid())

        if user_form.is_valid() and doctor_form.is_valid():
            print("Form is Valid")
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data["password"])
            user.role = "doctor"
            user.save()
            print("User Saved", user.id)

            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()
            print("Doctor Saved:", doctor.id)

            return redirect ("doctor_list")
        
    else:
        user_form = DoctorUserForm()
        doctor_form = DoctorForm()

        # print("User Form Errors: ", user_form.errors)
        # print("Doctor Form Errors: ", doctor_form.errors)
    
    return render(request,"doctors/doctor_form.html",{
        "user_form": user_form,
        "doctor_form": doctor_form
    })
    




def doctor_dashboard(request):
    return render(request, 'doctors/doctor_dashboard.html')
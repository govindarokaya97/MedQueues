from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import DoctorForm, DoctorUserForm, DoctorScheduleForm, DoctorLeaveForm
from .models import Doctor, Department, DoctorSchedule, DoctorLeave
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
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
            user.save()
            print("User Saved", user.id)

            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()
            print("Doctor Saved:", doctor.id)


            messages.success(request, "Doctor Added Successfully")
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



def doctor_detail(request,id):
    doctor = get_object_or_404(Doctor, id=id)
    context={
        "doctor": doctor
    }
    return render(request, "doctors/doctor_detail.html",context)



@login_required
def doctor_update(request, id):
    doctor = get_object_or_404(Doctor, id=id)

    if request.method == "POST":
        doctor_form = DoctorForm(request.POST, request.FILES, instance=doctor)

        if doctor_form.is_valid():
            doctor_form.save()
            messages.success(request, "Updated Successfully")
            return redirect("doctor_list")
    else:
        doctor_form = DoctorForm(instance=doctor)

    context = {
        "doctor": doctor,
        "doctor_form": doctor_form,
    }

    return render(request, "doctors/doctor_form.html", context)



def doctor_delete(request, id):
    doctor = get_object_or_404(Doctor, id=id)

    if request.method == "POST":
        doctor.delete()
        messages.success(request, "Deleted Successfully")
        return redirect("doctor_list")
    context={
        "doctor":doctor
    }

    return render(request, "doctors/doctor_confirm_delete.html", context)


# ---------------------------------------------------------------------------
# Weekly schedule
# ---------------------------------------------------------------------------

@login_required
def doctor_schedule(request, id):
    doctor = get_object_or_404(Doctor, id=id)

    if request.method == "POST":
        form = DoctorScheduleForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.doctor = doctor
            try:
                slot.full_clean()
                slot.save()
                messages.success(request, "Slot added successfully")
            except Exception as e:
                for msgs in getattr(e, "message_dict", {"__all__": [str(e)]}).values():
                    for m in msgs:
                        messages.error(request, m)
            return redirect("doctor_schedule", id=doctor.id)
    else:
        form = DoctorScheduleForm()

    context = {
        "doctor": doctor,
        "form": form,
        "slots": doctor.schedules.all(),
    }
    return render(request, "doctors/doctor_schedule.html", context)


@login_required
def doctor_schedule_delete(request, id, slot_id):
    doctor = get_object_or_404(Doctor, id=id)
    slot = get_object_or_404(DoctorSchedule, id=slot_id, doctor=doctor)

    if request.method == "POST":
        slot.delete()
        messages.success(request, "Slot removed")
    return redirect("doctor_schedule", id=doctor.id)


# ---------------------------------------------------------------------------
# Leave requests
# ---------------------------------------------------------------------------

@login_required
def leave_request_create(request, id):
    doctor = get_object_or_404(Doctor, id=id)

    if request.method == "POST":
        form = DoctorLeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.doctor = doctor
            try:
                leave.full_clean()
                leave.save()
                messages.success(request, "Leave request submitted")
                return redirect("doctor_detail", id=doctor.id)
            except Exception as e:
                for msgs in getattr(e, "message_dict", {"__all__": [str(e)]}).values():
                    for m in msgs:
                        messages.error(request, m)
    else:
        form = DoctorLeaveForm()

    context = {"doctor": doctor, "form": form}
    return render(request, "doctors/leave_form.html", context)


@login_required
def leave_list(request):
    status = request.GET.get("status", "")

    leaves = DoctorLeave.objects.all()

    if status:
        leaves = leaves.filter(status=status)

    context = {
        "leaves": leaves,
        "status": status,
    }

    return render(request, "doctors/leave_list.html", context)

@login_required
def leave_review(request, id, action):

    from django.utils import timezone

    leave = get_object_or_404(DoctorLeave, id=id)

    if request.method == "POST" and action in ("approve", "reject"):
        leave.status = "Approved" if action == "approve" else "Rejected"
        leave.reviewed_at = timezone.now()
        leave.reviewed_by = request.user
        leave.save()
        messages.success(request, f"Leave {leave.status.lower()}")

    return redirect("leave_list")

@login_required
def dashboard_view(request):
    context = {
        "total_patients": Patient.objects.count(),
        "total_doctors": Doctor.objects.count(),
        "appointments_today": Appointment.objects.filter(appointment_date=timezone.now().date()).count(),
    }
    return render(request, 'dashboard/dashboard.html', context)
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import DoctorScheduleForm, DoctorLeaveForm, DoctorUserForm, DoctorForm
from .models import Doctor, Department, DoctorSchedule, DoctorLeave
from django.contrib import messages
from django.utils import timezone
from appointments.models import Appointment
from patients.models import Patient
from accounts.models import CustomUser
from accounts.utils import generate_username
from accounts.decorators import role_required
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.core.paginator import Paginator


# Create your views here.
@role_required("admin")
def doctor_list(request):
    doctors = Doctor.objects.select_related(
        "user",
        "department"
    ).all()

    search = request.GET.get("search")
    department_id = request.GET.get("department")   # Selected department from URL
    departments = Department.objects.all()          # For dropdown/list

    if search:
        doctors = doctors.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(specialization__icontains=search)
        )

    if department_id:
        doctors = doctors.filter(department_id=department_id)

    paginator = Paginator(doctors, 10)
    page = request.GET.get("page")
    doctors = paginator.get_page(page)

    context={
        "doctors": doctors,
        "departments": departments,
        "search": search,
        "selected_department": department_id,
    }
    return render(request, "doctors/doctor_list.html", context)


@role_required("admin")
def doctor_create(request):
    password = get_random_string(10)

    if request.method == "POST":

        user_form = DoctorUserForm(request.POST)
        doctor_form = DoctorForm(request.POST, request.FILES)

        if user_form.is_valid() and doctor_form.is_valid():

            username = generate_username("DR")

            user = CustomUser.objects.create_user(
                username=username,
                password = password,
                role="doctor",
                first_name=user_form.cleaned_data["first_name"],
                last_name=user_form.cleaned_data["last_name"],
                email=user_form.cleaned_data["email"],
            )

            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()
            

            messages.success(
                request,
                f"Doctor created.\nUsername: {username}\nPassword: {password}"
                )

            return redirect("doctor_list")

    else:
        user_form = DoctorUserForm()
        doctor_form = DoctorForm()

    return render(
        request,
        "doctors/doctor_form.html",
        {
            "user_form": user_form,
            "doctor_form": doctor_form,

        }
    )



@role_required("admin", "doctor")
def doctor_detail(request, id):
    if request.user.role == "doctor":
        doctor = get_object_or_404(Doctor, user=request.user)
    else:
        doctor = get_object_or_404(Doctor, id=id)

    return render(
        request,
        "doctors/doctor_detail.html",
        {"doctor": doctor},
    )



@role_required("admin")
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



@role_required("admin")
def doctor_delete(request, id):
    doctor = get_object_or_404(Doctor, id=id)

    if request.method == "POST":
        doctor.delete()
        messages.success(request, "Deleted successfully.")
        return redirect("doctor_list")

    return render(
        request,
        "doctors/doctor_confirm_delete.html",
        {"doctor": doctor},
    )


@role_required("admin","doctor")
def doctor_schedule(request, id):
    if request.user.role == "doctor":
        doctor = get_object_or_404(
            Doctor.objects.select_related("user", "department"),
            user=request.user,
        )
    else:
        doctor = get_object_or_404(
            Doctor.objects.select_related("user", "department"),
            id=id,
        )

    if request.method == "POST":
        form = DoctorScheduleForm(request.POST)

        if form.is_valid():
            slot = form.save(commit=False)
            slot.doctor = doctor

            try:
                slot.full_clean()
                slot.save()
                messages.success(request, "Slot added successfully")
                return redirect("doctor_schedule", id=doctor.id)

            except ValidationError as e:
                for msgs in getattr(e, "message_dict", {"__all__": [str(e)]}).values():
                    
                    for m in msgs:
                        messages.error(request, m)

    else:
        form = DoctorScheduleForm()

    context = {
        "doctor": doctor,
        "form": form,
        "slots": doctor.schedules.order_by("day_of_week", "start_time"),
    }
    return render(request, "doctors/doctor_schedule.html", context)


@role_required("admin","doctor")
def doctor_schedule_delete(request, id, slot_id):
    if request.user.role == "doctor":
        doctor = get_object_or_404(Doctor, user=request.user)
    else:
        doctor = get_object_or_404(Doctor, id=id)

    slot = get_object_or_404(DoctorSchedule, id=slot_id, doctor=doctor)

    if request.method == "POST":
        slot.delete()
        messages.success(request, "Slot removed")
    return redirect("doctor_schedule", id=doctor.id)


@role_required("doctor")
def leave_request_create(request, id):
    if request.user.role == "doctor":
        doctor = get_object_or_404(Doctor, user=request.user)
    else:
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
            except ValidationError as e:
                for msgs in getattr(e, "message_dict", {"__all__": [str(e)]}).values():
                    for m in msgs:
                        messages.error(request, m)
    else:
        form = DoctorLeaveForm()

    context = {"doctor": doctor, "form": form}
    return render(request, "doctors/leave_form.html", context)


@role_required("admin")
def leave_list(request):
    status = request.GET.get("status", "")

    leaves = DoctorLeave.objects.select_related(
        "doctor",
        "reviewed_by",
        ).order_by("-requested_at")

    if status:
        leaves = leaves.filter(status=status)

    context = {
        "leaves": leaves,
        "status": status,
    }

    return render(request, "doctors/leave_list.html", context)



@role_required("admin")
def leave_review(request, id, action):
    leave = get_object_or_404(DoctorLeave, id=id)

    if request.method == "POST" and action in ("approve", "reject"):
        leave.status = "Approved" if action == "approve" else "Rejected"
        leave.reviewed_at = timezone.now()
        leave.reviewed_by = request.user
        leave.save()
        messages.success(request, f"Leave {leave.status.lower()}")

    return redirect("leave_list")



@role_required("doctor")
def dashboard_view(request):
    doctor = get_object_or_404(Doctor, user=request.user)

    today = timezone.now().date()

    appointments_today = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=today,
    )

    pending = appointments_today.filter(status="Pending").count()
    today_count = appointments_today.count()
    upcoming = Appointment.objects.filter(doctor=doctor,appointment_date__gte=today)
    completed_today = appointments_today.filter(
    status="Completed"
    ).count()

    pending_today = appointments_today.filter(
        status="Pending"
    ).count()

    context = {
        "doctor": doctor,
        "today": today_count,
        "pending": pending,
        "completed_today": completed_today,
        "pending_today": pending_today,
        "upcoming": upcoming.count(),
        "upcoming": upcoming.count(),
        "today_appointments": appointments_today[:5],
        "total_doctors": Doctor.objects.count(),
        "recent_patients": Patient.objects.select_related("user").order_by("-created_at")[:5],
        "total_patients": Patient.objects.count(),
        }

    return render(request, "doctors/doctor_dashboard.html", context)


@role_required("doctor")
def doctor_profile(request):
    doctor = request.user.doctor

    return render(request, "doctors/doctor_profile.html", {"doctor":doctor})
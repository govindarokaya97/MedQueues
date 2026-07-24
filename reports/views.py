from django.shortcuts import render, redirect, get_object_or_404

from django.db.models import Sum, Q
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from laboratory.models import LabRequest
from pharmacy.models import Medicine
from billing.models import Bill



def dashboard(request):

    context = {

        "patient_count": Patient.objects.count(),

        "doctor_count": Doctor.objects.count(),

        "appointment_count": Appointment.objects.count(),

        "lab_request_count": LabRequest.objects.count(),

        "medicine_count": Medicine.objects.count(),

        "bill_count": Bill.objects.count(),

        "total_revenue": (
            Bill.objects.filter(
                payment_status="Paid"
            ).aggregate(
                total=Sum("total_amount")
            )["total"] or 0
        ),

    }

    return render(
        request,
        "reports/dashboard.html",
        context,
    )
    
    

def patient_report(request):

    patients = Patient.objects.all().order_by("-created_at")

    search = request.GET.get("search")

    gender = request.GET.get("gender")

    blood_group = request.GET.get("blood_group")

    if search:

        patients = patients.filter(

            Q(user__first_name__icontains=search) |

            Q(user__last_name__icontains=search) |

            Q(user__phone__icontains=search)

        )

    if gender:

        patients = patients.filter(gender=gender)

    if blood_group:

        patients = patients.filter(
            blood_group=blood_group
        )

    context = {

        "patients": patients,

    }

    return render(
        request,
        "reports/patient_report.html",
        context
    )
    
    
    
def patient_report_detail(request, id):

    patient = get_object_or_404(Patient, id=id)

    appointments = patient.appointments.all()

    prescriptions = patient.prescriptions.all()

    lab_requests = patient.lab_requests.all()

    bills = patient.bills.all()

    context = {

        "patient": patient,

        "appointments": appointments,

        "prescriptions": prescriptions,

        "lab_requests": lab_requests,

        "bills": bills,

        "appointment_count": appointments.count(),

        "completed_count": appointments.filter(

            status="Completed"

        ).count(),

        "prescription_count": prescriptions.count(),

        "lab_request_count": lab_requests.count(),

        "bill_count": bills.count(),

        "paid_bill_count": bills.filter(

            payment_status="Paid"

        ).count(),

        "pending_bill_count": bills.filter(

            payment_status="Pending"

        ).count(),

        "total_paid": bills.filter(

            payment_status="Paid"

        ).aggregate(

            total=Sum("total_amount")

        )["total"] or 0,

    }

    return render(

        request,

        "reports/patient_report_detail.html",

        context,

    )



def doctor_report(request):

    doctors = Doctor.objects.all().order_by("full_name")

    search = request.GET.get("search")

    specialization = request.GET.get("specialization")

    if search:

        doctors = doctors.filter(

            Q(full_name__icontains=search) |

            Q(user__email__icontains=search)

        )

    if specialization:

        doctors = doctors.filter(

            specialization=specialization

        )

    context = {

        "doctors": doctors,

        "specializations": Doctor.objects.values_list(

            "specialization",

            flat=True

        ).distinct()

    }

    return render(

        request,

        "reports/doctor_report.html",

        context,

    )
    

def doctor_report_detail(request, id):

    doctor = get_object_or_404(

        Doctor,

        id=id

    )

    appointments = doctor.appointments.all()

    prescriptions = doctor.prescriptions.all()

    lab_requests = doctor.labrequest_set.all()

    completed_appointments = appointments.filter(

        status="Completed"

    )

    total_revenue = (

        completed_appointments.count()

        * doctor.consultation_fee

    )

    context = {

        "doctor": doctor,

        "appointments": appointments,

        "prescriptions": prescriptions,

        "lab_requests": lab_requests,

        "appointment_count": appointments.count(),

        "completed_count": completed_appointments.count(),

        "prescription_count": prescriptions.count(),

        "lab_request_count": lab_requests.count(),

        "total_revenue": total_revenue,

    }

    return render(

        request,

        "reports/doctor_report_detail.html",

        context,

    )
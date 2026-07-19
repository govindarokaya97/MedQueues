from django.shortcuts import redirect
from django.db.models import Sum, Count, F
from django.utils import timezone
from django.views.generic import TemplateView

from accounts.decorators import role_required
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from billing.models import Bill
from pharmacy.models import Medicine, Prescription
from laboratory.models import LabRequest, LabReport



class DashboardView(TemplateView):
    template_name = "dashboard/dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        if request.user.role != "admin":
            return redirect("dashboard")

        return super().dispatch(request, *args, **kwargs)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.now().date()

        # Basic counts
        context["patient_count"] = Patient.objects.count()
        context["doctor_count"] = Doctor.objects.count()
        context["appointment_count"] = Appointment.objects.count()
        context["medicine_count"] = Medicine.objects.count()
        context["lab_request_count"] = LabRequest.objects.count()

        # Billing counts
        context["bill_count"] = Bill.objects.count()

        context["paid_bill_count"] = Bill.objects.filter(
            payment_status="Paid"
        ).count()

        context["pending_bill_count"] = Bill.objects.filter(
            payment_status="Pending"
        ).count()

        # Recent payments
        context["recent_payments"] = (
            Bill.objects
            .filter(payment_status="Paid")
            .select_related("patient")
            .order_by("-payment_date")[:5]
        )
        
        context["total_bills"] = Bill.objects.count()
        
        context["cancelled_bills"] = Bill.objects.filter(
            payment_status="Pending").count()
        


        # Payment methods
        context["payment_methods"] = (
            Bill.objects
            .filter(payment_status="Paid")
            .values("payment_method")
            .annotate(total=Count("id"))
        )
        
        # Total Revenue
        context["total_revenue"] = (
            Bill.objects.filter(
                payment_status ="Paid"
            ).aggregate(
                total=Sum("total_amount")
            )["total"] or 0
        )
        
        # Today's revenue
        context["today_revenue"] = (
            Bill.objects
            .filter(
                payment_status="Paid",
                payment_date__date=today
            )
            .aggregate(
                total=Sum("total_amount")
            )["total"] or 0
        )

        # Monthly revenue
        context["monthly_revenue"] = (
            Bill.objects
            .filter(
                payment_status="Paid",
                payment_date__year=today.year,
                payment_date__month=today.month
            )
            .aggregate(
                total=Sum("total_amount")
            )["total"] or 0
        )
        
        # Recent Appointments
        context["recent_appointments"]=(
            Appointment.objects.filter(
                appointment_date=today).select_related(
                    "patient","doctor").order_by(
                        '-appointment_date',
                        '-appointment_time',
                    )
                )
        
        
        # Recent Prescriptions
        context["recent_prescriptions"] = {
            Prescription.objects.select_related(
                "patient", "doctor"
            ).order_by("-created_at")[:5]
        }
        
        

        
        
        # Recent Bills
        context["recent_bills"] = {
            Bill.objects.select_related(
                "patient", "doctor"
            ).order_by("-created_at")[:5]
        }
        
        
        # Medicines Statictics
        context["total_medicines"] = Medicine.objects.count()
        
        context["available_medicines"] = (
            Medicine.objects.filter(stock_quantity__gt=0).count()
        )
        
        context["out_of_stock"] = (
            Medicine.objects.filter(stock_quantity=0).count()
        )
        
        context["low_stock"] = (
            Medicine.objects.filter(
                stock_quantity__lte=F("reorder_level"),
                stock_quantity__gt=0
            ).count()
        )
        
        context["low_stock_medicines"]=(
            Medicine.objects.filter(
                stock_quantity__lte=F("reorder_level"),
                stock_quantity__gt=0,
            ).order_by("stock_quantity")
        )

        
        # Laboratory Statistics

        context["total_lab_requests"] = LabRequest.objects.count()

        context["pending_lab_requests"] = (
            LabRequest.objects.filter(
                status="Pending"
            ).count()
        )

        context["processing_lab_requests"] = (
            LabRequest.objects.filter(
                status="Processing"
            ).count()
        )

        context["completed_lab_requests"] = (
            LabRequest.objects.filter(
                status="Completed"
            ).count()
        )

        context["total_lab_reports"] = LabReport.objects.count()
        
                # Recent LabRequests
        context["recent_lab_requests"] = (
            LabRequest.objects
            .select_related(
                "patient",
                "doctor",
                "assigned_to",
            )
            .order_by("-requested_date")[:5]
        )
        
        
        context["recent_lab_reports"] = (
            LabReport.objects
            .select_related(
                "lab_request",
                "technician",
            )
            .order_by("-generated_at")[:5]
        )
        
        
        context["verified_reports"] = (
            LabReport.objects.filter(
                verified_at__isnull=False
            ).count()
        )

        context["pending_verification"] = (
            LabReport.objects.filter(
                verified_at__isnull=True
            ).count()
        )
                


        
        return context 


    

    
    
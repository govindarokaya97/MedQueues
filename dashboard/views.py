from django.shortcuts import redirect
from django.db.models import Sum, Count
from django.utils import timezone
from django.views.generic import TemplateView

from accounts.decorators import role_required
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from billing.models import Bill
from pharmacy.models import Medicine
from laboratory.models import LabRequest

from .sevices import get_billing_statistics


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
        
        context.update(get_billing_statistics())


        return context
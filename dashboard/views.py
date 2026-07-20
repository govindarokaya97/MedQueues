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

from collections import OrderedDict
import json


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

        # =========================
        # BASIC COUNTS
        # =========================

        context["patient_count"] = Patient.objects.count()
        context["doctor_count"] = Doctor.objects.count()
        context["appointment_count"] = Appointment.objects.count()
        context["medicine_count"] = Medicine.objects.count()
        context["lab_request_count"] = LabRequest.objects.count()

        # =========================
        # BILLING COUNTS
        # =========================

        bill_count = Bill.objects.count()

        paid_bill_count = Bill.objects.filter(
            payment_status="Paid"
        ).count()

        pending_bill_count = Bill.objects.filter(
            payment_status="Pending"
        ).count()

        cancelled_bill_count = Bill.objects.filter(
            payment_status="Cancelled"
        ).count()

        context["bill_count"] = bill_count
        context["paid_bill_count"] = paid_bill_count
        context["pending_bill_count"] = pending_bill_count
        context["cancelled_bills"] = cancelled_bill_count

        # =========================
        # RECENT PAYMENTS
        # =========================

        context["recent_payments"] = (
            Bill.objects
            .filter(payment_status="Paid")
            .select_related("patient")
            .order_by("-payment_date")[:5]
        )

        # =========================
        # REVENUE
        # =========================

        total_revenue = (
            Bill.objects
            .filter(payment_status="Paid")
            .aggregate(total=Sum("total_amount"))["total"] or 0
        )

        today_revenue = (
            Bill.objects
            .filter(
                payment_status="Paid",
                payment_date__date=today
            )
            .aggregate(total=Sum("total_amount"))["total"] or 0
        )

        monthly_revenue = (
            Bill.objects
            .filter(
                payment_status="Paid",
                payment_date__year=today.year,
                payment_date__month=today.month
            )
            .aggregate(total=Sum("total_amount"))["total"] or 0
        )

        context["total_revenue"] = total_revenue
        context["today_revenue"] = today_revenue
        context["monthly_revenue"] = monthly_revenue

        # =========================
        # APPOINTMENTS
        # =========================

        context["recent_appointments"] = (
            Appointment.objects
            .select_related("patient", "doctor")
            .order_by("-appointment_date", "-appointment_time")[:5]
        )

        context["today_appointments"] = (
            Appointment.objects
            .filter(appointment_date=today)
            .select_related("patient", "doctor")
            .order_by("appointment_time")
        )

        # =========================
        # PRESCRIPTIONS
        # =========================

        context["recent_prescriptions"] = (
            Prescription.objects
            .select_related("patient", "doctor")
            .order_by("-created_at")[:5]
        )

        # =========================
        # RECENT BILLS
        # =========================

        context["recent_bills"] = (
            Bill.objects
            .select_related("patient")
            .order_by("-created_at")[:5]
        )

        # =========================
        # MEDICINES
        # =========================

        context["total_medicines"] = Medicine.objects.count()

        context["out_of_stock"] = Medicine.objects.filter(
            stock_quantity=0
        ).count()

        context["low_stock"] = Medicine.objects.filter(
            stock_quantity__lte=F("reorder_level"),
            stock_quantity__gt=0
        ).count()

        context["low_stock_medicines"] = (
            Medicine.objects
            .filter(
                stock_quantity__lte=F("reorder_level"),
                stock_quantity__gt=0
            )
            .order_by("stock_quantity")
        )

        # =========================
        # LABORATORY
        # =========================

        total_lab_requests = LabRequest.objects.count()

        pending_lab_requests = LabRequest.objects.filter(
            status="Pending"
        ).count()

        processing_lab_requests = LabRequest.objects.filter(
            status="Processing"
        ).count()

        completed_lab_requests = LabRequest.objects.filter(
            status="Completed"
        ).count()

        context["total_lab_requests"] = total_lab_requests
        context["pending_lab_requests"] = pending_lab_requests
        context["processing_lab_requests"] = processing_lab_requests
        context["completed_lab_requests"] = completed_lab_requests
        context["total_lab_reports"] = LabReport.objects.count()

        context["recent_lab_requests"] = (
            LabRequest.objects
            .select_related("patient", "doctor", "assigned_to")
            .order_by("-requested_date")[:5]
        )

        context["recent_lab_reports"] = (
            LabReport.objects
            .select_related("lab_request", "technician")
            .order_by("-generated_at")[:5]
        )

        context["verified_reports"] = LabReport.objects.filter(
            verified_at__isnull=False
        ).count()

        context["pending_verification"] = LabReport.objects.filter(
            verified_at__isnull=True
        ).count()

        # =========================
        # CHART DATA
        # =========================

        context["billing_labels"] = json.dumps([
            "Paid",
            "Pending",
            "Cancelled",
        ])

        context["billing_values"] = json.dumps([
            paid_bill_count,
            pending_bill_count,
            cancelled_bill_count,
        ])

        # Revenue chart
        context["revenue_labels"] = json.dumps([
            "Total Revenue",
            "Today's Revenue",
            "Monthly Revenue",
        ])

        context["revenue_values"] = json.dumps([
            float(total_revenue),
            float(today_revenue),
            float(monthly_revenue),
        ])

        # Appointment chart
        appointment_status = (
            Appointment.objects
            .values("status")
            .annotate(total=Count("id"))
        )

        context["appointment_labels"] = json.dumps([
            item["status"]
            for item in appointment_status
        ])

        context["appointment_values"] = json.dumps([
            item["total"]
            for item in appointment_status
        ])

        # Laboratory chart
        context["lab_labels"] = json.dumps([
            "Pending",
            "Processing",
            "Completed",
        ])

        context["lab_values"] = json.dumps([
            pending_lab_requests,
            processing_lab_requests,
            completed_lab_requests,
        ])

        return context

    
    
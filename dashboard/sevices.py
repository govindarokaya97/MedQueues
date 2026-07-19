from django.db.models import Sum
from billing.models import Bill
from django.utils import timezone

from appointments.models import Appointment

def get_dashboard_statistics():
    today = timezone.now().date()

    return {
        "total_bills": Bill.objects.count(),
        "paid_bills": Bill.objects.filter(payment_status="Paid").count(),
        "pending_bills": Bill.objects.filter(payment_status="Pending").count(),
        "cancelled_bills": Bill.objects.filter(payment_status="Cancelled").count(),
        "total_revenue": Bill.objects.filter(
            payment_status="Paid"
        ).aggregate(total=Sum("total_amount"))["total"] or 0,
        "today_revenue": Bill.objects.filter(
            payment_status="Paid",
            payment_date__date=today,
        ).aggregate(total=Sum("total_amount"))["total"] or 0,
    }
    
def get_today_appointments():
    
    today = timezone.now().date()
    
    return(
        Appointment.objects.filter(
            appointment_date=today
        ).select_related(
            "patient",
            "doctor",
        ).order_by("appointment_id")
    )
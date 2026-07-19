from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse
from decimal import Decimal
from django.db.models import Sum
from django.utils import timezone

from .models import Bill


def generate_invoice_pdf(request, bill):

    html = render_to_string(
        "billing/invoice_pdf.html",
        {
            "bill": bill
        }
    )

    pdf = HTML(
        string=html,
        base_url=request.build_absolute_uri()
    ).write_pdf()

    response = HttpResponse(
        pdf,
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = f'attachment; filename="{bill.invoice_number}.pdf"'

    return response



def total_revenue():
    return (
        Bill.objects.filter(payment_status= "Paid").aggregate(
            total=Sum("total_amount"))["total"] or Decimal("0.00")
    )
    
def today_revenue():
    today = timezone.now().date()
    
    return (
        Bill.objects.filter(
            payment_status="Paid",
            payment_date__date=today,).aggregate(
                total=Sum("total_amount"))
            ["total"] or Decimal("0.00")
    )

def monthly_revenue():
    today = timezone.now().date()
    
    return (
        Bill.objects.filter(
            payment_status="Paid",
            payment_date__year=today.year,
            payment_date__month=today.month,  
            ).aggregate(
                total=Sum("total_amount"))
            ["total"] or Decimal("0.00")
    )

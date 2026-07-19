from django.shortcuts import (render, redirect, get_object_or_404)

from .models import Bill
from .forms import BillForm, BillPaymentForm
from django.urls import reverse_lazy
from django.views.generic import (ListView, UpdateView, DeleteView, DetailView )

from appointments.models import Appointment
from .services import generate_bill
from django.utils import timezone

from django.views.decorators.http import require_POST
from .utils import generate_invoice_pdf


class BillListView(ListView):
    model = Bill
    template_name = "billing/bill_list.html"
    context_object_name = "bills"
    ordering = ["-created_at"]
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            "patient",
            "appointment"
        )
        
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                invoice_number__icontains=search
            )
        
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(
                payment_status=status
            )
        
        return queryset
        
 
class BillDetailView(DetailView):
    model = Bill
    pk_url_kwarg = "id"
    template_name = "billing/bill_detail.html"
    
    def get_queryset(self):
        return Bill.objects.select_related(
            "patient",
            "appointment",
            "appointment__doctor",
        ).prefetch_related("items")


class BillPaymentView(UpdateView):
    
    model = Bill
    form_class = BillPaymentForm
    pk_url_kwarg = "id"
    template_name = "billing/payment_form.html"
    
    def form_valid(self, form):
        bill = form.save(commit=False)
        
        if bill.payment_status == "Paid":
            bill.payment_date = timezone.now()
        
        bill.save()
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy(
            "bill_detail",
            kwargs={"id": self.object.id}
        )

class BillUpdateView(UpdateView):
    model = Bill
    pk_url_kwarg = "id"

    fields = [
        "amount",
        "discount",
        "tax",
        "payment_method",
        "payment_status",
        "notes",
    ]

    template_name = "billing/bill_form.html"
    success_url = reverse_lazy("bill_list")


class BillDeleteView(DeleteView):
    model = Bill
    pk_url_kwarg = "id"
    template_name = "billing/bill_confirm_delete.html"
    success_url = reverse_lazy("bill_list")


def create_bill(request, appointment_id):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )

    bill = generate_bill(
        appointment
    )

    return redirect(
        "bill_detail",
        id=bill.id
    )
    
    
    
@require_POST
def mark_bill_paid(request, id):
    bill = get_object_or_404(Bill, id=id)
    
    if bill.payment_status != "Paid":
        bill.payment_status = "Paid"
        
        if not bill.payment_date:
            bill.payment_date = timezone.now()
            
        bill.save(update_fields=[
            "payment_status",
            "payment_date",
        ])
    
    return redirect("bill_detail", id=bill.id)




def bill_pdf(request,id):
    
    bill = get_object_or_404(
        Bill,
        id=id
    )
    
    return generate_invoice_pdf( request,bill)
    
        
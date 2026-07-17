from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from .models import Bill
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    UpdateView,
    DeleteView,
    DetailView
)

from appointments.models import Appointment
from .services import generate_bill


class BillListView(ListView):
    model = Bill
    template_name = "billing/bill_list.html"
    context_object_name = "bills"

 
class BillDetailView(DetailView):
    model = Bill
    pk_url_kwarg = "id"
    template_name = "billing/bill_detail.html"


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
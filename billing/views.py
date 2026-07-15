from django.shortcuts import render, get_list_or_404
from .models import Bill
from django.urls import reverse_lazy
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView, DetailView)
from appointments.models import Appointment

# Create your views here.

class BillListView(ListView):
    model = Bill
    template_name = "billing/bill_list.html"
    context_object_name = "bills"


class BillCreateView(CreateView):
    model = Bill
    fields = [
        "patient",
        "appointment",
        "amount",
        "discount",
        "tax",
        "payment_method",
        "payment_status",
        "notes",
    ]

    template_name = "billing/bill_form.html"
    success_url = reverse_lazy("bill_list")


class BillDetailView(DetailView):
    model = Bill
    template_name = "billing/bill_detail.html"


class BillUpdateView(UpdateView):
    model = Bill
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
    template_name = "billing/bill_confirm_delete.html"
    success_url = reverse_lazy("bill_list")


def generate_bill(request, appointment_id):
    appointments = get_list_or_404(
        Appointment,
        id = appointment_id
    )

    bill = Bill.objects.create(
        patient=appointment.patient,
        appointment=appointment,
        amount=appointment.doctor.consultation_fee,
        discount=0,
        tax=0,
        payment_method="Cash",
        payment_status="Pending"
    )

    return render("bill_detail", id=bill.id)


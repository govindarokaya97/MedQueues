from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Medicine, MedicineCategory, StockTransaction, Prescription
from .forms import MedicineForm, StockTransactionForm, PrescriptionForm, PrescriptionItemFormSet
from django.db.models import Q
from django.contrib import messages
from appointments.models import Appointment
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse


# Create your views here.

class MedicineListView(ListView):
    model = Medicine
    template_name = "pharmacy/medicine_list.html"
    context_object_name = "medicines"
    paginate_by = 10
    
    
    def get_queryset(self):
        queryset = Medicine.objects.all()
        
        search = self.request.GET.get("search")
            
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(generic_name__icontains=search) |
                Q(batch_number__icontains=search) |
                Q(manufacturer__icontains=search)
            )
        
        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category_id=category)
            
        return queryset.order_by("name")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_category = self.request.GET.get("category", "")
        context["category_options"] = [
            {"id": c.id, "name": c.name, "is_selected": str(c.id) == selected_category}
            for c in MedicineCategory.objects.all()
        ]
        return context
    
    
    
class MedicineDetailView(DetailView):
    model = Medicine
    pk_url_kwarg = "id"
    template_name = "pharmacy/medicine_detail.html"


def medicine_details(medicine_id):
    try:
        medicine = Medicine.objects.get(id=medicine_id)

        return JsonResponse({
            "name": medicine.name,
            "generic_name": medicine.generic_name,
            "category": (
                medicine.category.name
                if medicine.category
                else ""
            ),
            "manufacturer": medicine.manufacturer,
            "batch_number": medicine.batch_number or "",
            "price": str(medicine.price),
            "stock": medicine.stock_quantity,
            "expiry_date": (
                medicine.expiry_date.strftime("%Y-%m-%d")
                if medicine.expiry_date
                else ""
            ),
            "is_expired": medicine.is_expired,
        })

    except Medicine.DoesNotExist:
        return JsonResponse(
            {"error": "Medicine not found"},
            status=404
        )
        
class MedicineCreateView(CreateView):
    model = Medicine
    form_class = MedicineForm
    template_name = "pharmacy/medicine_form.html"
    success_url = reverse_lazy("medicine_list")
    
    
class MedicineUpdateView(UpdateView):
    model = Medicine
    pk_url_kwarg = "id"
    form_class = MedicineForm
    template_name = "pharmacy/medicine_form.html"
    success_url = reverse_lazy("medicine_list")
    
    
class MedicineDeleteView(DeleteView):
    model = Medicine
    pk_url_kwarg = "id"
    template_name = "pharmacy/medicine_confirm_delete.html"
    success_url = reverse_lazy("medicine_list")
    
    
class StockTransactionCreativeView(CreateView):
        
    model = StockTransaction    
    form_class = StockTransactionForm
    template_name = "pharmacy/stock_transaction_form.html"
    
    success_url = reverse_lazy("medicine_list")
    transaction_type = "STOCK_OUT"
        
    def form_valid(self, form):
        form.instance.performed_by = self.request.user
        response = super().form_valid(form)

        messages.success(
            self.request,
            "Stock updated successfully"
        )

        return response
        
            
@transaction.atomic
def prescription_create(request, appointment_id):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )


    # Prevent duplicate prescription
    if hasattr(appointment, "prescription"):

        messages.info(
            request,
            "A prescription already exists for this appointment."
        )

        return redirect(
            "prescription_detail",
            id=appointment.prescription.id
        )


    if request.method == "POST":

        form = PrescriptionForm(
            request.POST
        )

        formset = PrescriptionItemFormSet(
            request.POST
        )


        if form.is_valid() and formset.is_valid():

            prescription = form.save(
                commit=False
            )


            # Automatically assign appointment details
            prescription.appointment = appointment
            prescription.patient = appointment.patient
            prescription.doctor = appointment.doctor


            prescription.save()


            # Save medicine items
            formset.instance = prescription
            items = formset.save()

            # Deduct the prescribed quantity from stock now that
            # the items are confirmed, and keep an audit trail.
            for item in items:
                medicine = item.medicine
                medicine.stock_quantity -= item.quantity
                medicine.save(update_fields=["stock_quantity"])

                StockTransaction.objects.create(
                    medicine=medicine,
                    transaction_type=StockTransaction.STOCK_OUT,
                    quantity=item.quantity,
                    remarks=f"Prescription #{prescription.id}",
                    performed_by=request.user,
                )

            messages.success(
                request,
                "Prescription created successfully."
            )


            return redirect(
                "prescription_detail",
                id=prescription.id
            )


    else:

        form = PrescriptionForm()

        formset = PrescriptionItemFormSet()


    return render(
        request,
        "pharmacy/prescription_create.html",
        {
            "form": form,
            "formset": formset,
            "appointment": appointment,
        }
    )
    
    
    
def prescription_list(request):

    prescriptions = Prescription.objects.select_related(
        "appointment",
        "patient",
        "doctor",
    ).prefetch_related(
        "items__medicine"
    )


    appointments = Appointment.objects.select_related(
        "prescription",
        "patient",
        "doctor",
    )


    return render(
        request,
        "pharmacy/prescription_list.html",
        {
            "prescriptions": prescriptions,
            "appointments": appointments,
        }
    )



@transaction.atomic
def prescription_dispense(request, id):

    prescription = get_object_or_404(
        Prescription,
        id=id
    )


    if prescription.status == "Dispensed":

        messages.warning(
            request,
            "This prescription has already been dispensed."
        )

        return redirect(
            "prescription_detail",
            id=prescription.id
        )


    # Stock was already deducted when the prescription was created,
    # so dispensing just confirms hand-off to the patient.
    prescription.status = "Dispensed"

    prescription.save(
        update_fields=[
            "status"
        ]
    )


    messages.success(
        request,
        "Prescription dispensed successfully."
    )


    return redirect(
        "prescription_detail",
        id=prescription.id
    )


class PrescriptionDetailView(DetailView):

    model = Prescription

    pk_url_kwarg = "id"

    template_name = (
        "pharmacy/prescription_detail.html"
    )

    context_object_name = "prescription"


    def get_queryset(self):

        return Prescription.objects.select_related(
            "appointment",
            "patient",
            "doctor",
        ).prefetch_related(
            "items__medicine"
        )
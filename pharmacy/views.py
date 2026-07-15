from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Medicine, MedicineCategory, StockTransaction, Prescription
from .forms import MedicineForm, StockTransactionForm, PrescriptionForm
from django.db.models import Q
from django.contrib import messages

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
    template_name = "pharmacy/stock_transactin_form.html"
    
    success_url = reverse_lazy("medicine_list")
    
    def form_valid(self, form):
        form.instance.performed_by = self.request.user
        return super().form_valid(form)
    
        messages.success(self.request, "Stock updated successfully")
        
        return super().form_valid(form)
        
            
        

def prescription_list(request):
    prescriptions = Prescription.objects.all()
    
    return render(request, "pharmacy/prescription_list.html",{
        "prescriptions":prescriptions,
    })

def prescription_create(request):
    
    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect("prescription_list")
    
    else:
        form = PrescriptionForm()
        
    return render(request, "pharmacy/prescription_form.html",{
        "form":form,
    })
    

def prescription_dispense(request, id):
    
    prescription = get_object_or_404(Prescription, id=id)
    
    for item in prescription.items.all():
        medicine = item.medicine
        
        if medicine.stock_quantity < item.quantity:
            return render(request, "pharmacy/error.html",{
                "message":f"{medicine.name} is out of stock."
            })
        
        medicine.stock_quantity -= item.quantity
        medicine.save()
    
    prescription.status = "Dispensed"
    prescription.save()
    
    return redirect("prescription_list")
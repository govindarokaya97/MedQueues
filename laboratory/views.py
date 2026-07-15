from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import LabReport, LabTest

# Create your views here.

class TestListView(ListView):
    model = LabTest
    template_name = "laboratory/test_list.html"
    context_object_name = "tests"
    paginate_by = 10
    
    
    
class TestDetailView(DetailView):
    model = LabTest
    pk_url_kwarg = "id"
    template_name = "laboratory/test_detail.html"
    
    
    
class TestCreateView(CreateView):
    model = LabTest
    template_name = "laboratory/test_form.html"
    success_url = reverse_lazy("test_list")
    
    
class TestUpdateView(UpdateView):
    model = LabTest
    pk_url_kwarg = "id"
    template_name = "laboratory/test_form.html"
    success_url = reverse_lazy("test_list")
    
    
class MedicineDeleteView(DeleteView):
    model = LabTest
    pk_url_kwarg = "id"
    template_name = "laboratory/test_report.html"
    success_url = reverse_lazy("test_list")
    


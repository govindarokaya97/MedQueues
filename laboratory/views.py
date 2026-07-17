from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView,)
from django.contrib import messages
from django.utils import timezone

from .models import LabTest, LabRequest, LabRequestItem, LabReport
from .forms import (LabTestForm, LabRequestForm, LabRequestItemFormSet, AssignTechnicianForm,LabReportForm)

# =========================
# LAB TEST VIEWS
# =========================

class TestListView(ListView):
    model = LabTest
    template_name = "laboratory/test_list.html"
    context_object_name = "tests"
    paginate_by = 10


class TestDetailView(DetailView):
    model = LabTest
    pk_url_kwarg = "id"
    template_name = "laboratory/test_detail.html"
    context_object_name = "test"


class TestCreateView(CreateView):
    model = LabTest
    template_name = "laboratory/test_form.html"
    form_class = LabTestForm
    success_url = reverse_lazy("test_list")


class TestUpdateView(UpdateView):
    model = LabTest
    pk_url_kwarg = "id"
    template_name = "laboratory/test_form.html"
    form_class = LabTestForm
    success_url = reverse_lazy("test_list")


class TestDeleteView(DeleteView):
    model = LabTest
    pk_url_kwarg = "id"
    template_name = "laboratory/test_confirm_delete.html"
    success_url = reverse_lazy("test_list")


# =========================
# LAB REQUEST LIST
# =========================

class LabRequestListView(ListView):
    model = LabRequest
    template_name = "laboratory/request_list.html"
    context_object_name = "lab_requests"
    paginate_by = 10
    ordering = ["-requested_date"]


# =========================
# CREATE LAB REQUEST
# =========================

def create_lab_request(request):

    if request.method == "POST":

        form = LabRequestForm(request.POST)

        formset = LabRequestItemFormSet(
            request.POST,
            prefix="items"
        )

        if form.is_valid() and formset.is_valid():

            lab_request = form.save()

            formset.instance = lab_request
            formset.save()

            messages.success(
                request,
                "Lab request created successfully."
            )

            return redirect("request_list")

    else:

        form = LabRequestForm()

        formset = LabRequestItemFormSet(
            prefix="items"
        )

    return render(
        request,
        "laboratory/lab_request_form.html",
        {
            "form": form,
            "formset": formset,
        }
    )
    
    
    
def assign_technician(request, id):
    lab_request = get_object_or_404( LabRequest, id=id)
    
    if request.method == "POST":
        form = AssignTechnicianForm(
            request.POST,
            instance=lab_request
        )
        
        if form.is_valid():
            form.save()
            
            messages.success(request, "Technician assigned successfully.")
            return redirect("request_list")
    
    else:
        form = AssignTechnicianForm(
            instance=lab_request
        )
    
    return render(request, "laboratory/assign_technician.html",{
        "form":form,
        "lab_request":lab_request,
        }
    )
    
    

def create_lab_report(request, id):
    lab_request = get_object_or_404( LabRequest, id=id)
    
    report = getattr(lab_request, "report", None)
    
    if request.method == "POST":
        form = LabReportForm(
            request.POST,
            request.FILES,
            instance=report  
        )
        
        if form.is_valid():
            report = form.save(commit=False)
            
            report.lab_request = lab_request
            report.technician = request.user
            
            report.save()
            
            messages.success(request, "Lab report saved successfully.")
            
            return redirect("request_list")
    else:
        form = LabReportForm(instance=report)
        
    return render(request, "laboratory/report_form.html",{
        "form":form,
        "lab_request": lab_request,
    })
          
    
def report_detail(request, id):

    lab_request = get_object_or_404(
        LabRequest,
        id=id
    )

    report, created = LabReport.objects.get_or_create(
        lab_request=lab_request,
        defaults={
            "technician": request.user
        }
    )

    results = lab_request.items.select_related(
        "lab_test"
    )

    return render(
        request,
        "laboratory/report_detail.html",
        {
            "lab_request": lab_request,
            "report": report,
            "results": results,
        }
    ) 
    
    
def verify_report(request, id):
    
    report = get_object_or_404(
        LabReport,
        id=id
    )
    
    report.status="Verified"
    report.verified_by = request.user
    report.verified_at = timezone.now()
    
    report.save()
    
    messages.success(request, "Laboratory report verified successfully.")
    
    return redirect("report_detail", report.lab_request.id )
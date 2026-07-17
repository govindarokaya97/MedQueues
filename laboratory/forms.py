from django import forms
from .models import LabTest, LabRequest, LabRequestItem, LabReport
from django.forms import inlineformset_factory
from django.contrib.auth import get_user_model


User = get_user_model()


class LabTestForm(forms.ModelForm):
    class Meta:
        model = LabTest
        fields = [
            "name",
            "price",
            "code",
            "category",
            "description",
            "normal_range",
        ]

        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 3}
            ),
        }


class LabRequestForm(forms.ModelForm):
    class Meta:
        model = LabRequest
        fields = [
            "patient",
            "doctor",
            "appointment",
            "notes",
        ]


class LabRequestItemForm(forms.ModelForm):
    class Meta:
        model = LabRequestItem
        fields = [
            "lab_test",
            "remarks",
        ]


LabRequestItemFormSet = inlineformset_factory(
    LabRequest,
    LabRequestItem,
    form=LabRequestItemForm,
    extra=1,
    can_delete=True,
)


class AssignTechnicianForm(forms.ModelForm):
    class Meta:
        model = LabRequest
        fields =[
            "assigned_to",
            "status"
        ]



class LabReportForm(forms.ModelForm):
    class Meta:
        model = LabReport
        
        fields =[
            "report_summary",
            "remarks",
            "report_file",
            "report_image",
            "status",     
        ]
        
        widgets = {
            "report_summary": forms.Textarea(attrs={"rows":4}),
            "remarks" : forms.Textarea(attrs={"rows":3})
        }


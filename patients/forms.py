from django import forms
from .models import Patient
from accounts.models import CustomUser

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ["user"]

class PatientUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
        ]
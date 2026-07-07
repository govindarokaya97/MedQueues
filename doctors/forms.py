from django import forms
from django.contrib.auth import get_user_model
from models import Doctor

User = get_user_model()

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            "department",
            "specialization",
            "qualification",
            "experience",
            "consultation_fee",
            "phone",
            "adress",
            "available",
            "profile_photo",
        ]

class DoctorUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields =[
            "first_name",
            "last_name",
            "username",
            "email",
            "password"
        ]
    password = forms.CharField(widget=forms.PasswordInput())
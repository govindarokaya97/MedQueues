from django import forms
from django.contrib.auth import get_user_model
from .models import Doctor, DoctorSchedule, DoctorLeave

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
            "address",
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


class DoctorScheduleForm(forms.ModelForm):
    class Meta:
        model = DoctorSchedule
        fields = ["day", "start_time", "end_time", "is_available"]
        widgets = {
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }


class DoctorLeaveForm(forms.ModelForm):
    class Meta:
        model = DoctorLeave
        fields = ["start_date", "end_date", "reason"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }
from django import forms
from django.contrib.auth import get_user_model
from .models import Doctor, DoctorSchedule, DoctorLeave
from accounts.models import CustomUser

class DoctorUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
        ]

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
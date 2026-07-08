from django import forms 
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={"type":"date"})
    )

    appointment_time = forms.TimeField(
        widget=forms.TimeInput(attrs={"type":"time"})
    )

    class Meta:
        model = Appointment
        fields =[
            "patient",
            "doctor",
            "appointment_date",
            "appointment_time",
            "reason",
            "status",
        ]
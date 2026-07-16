from django import forms
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )

    appointment_time = forms.TimeField(
        widget=forms.TimeInput(attrs={"type": "time"})
    )

    class Meta:
        model = Appointment
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        doctor = cleaned_data.get("doctor")
        appointment_date = cleaned_data.get("appointment_date")
        appointment_time = cleaned_data.get("appointment_time")

        if doctor and appointment_date and appointment_time:

            exists = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
            )

            if self.instance.id:
                exists = exists.exclude(id=self.instance.pk)

            if exists.exists():
                raise forms.ValidationError(
                    "This doctor already has an appointment at this time."
                )

        return cleaned_data
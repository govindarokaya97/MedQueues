from django.db import models
from patients.models import Patient
from doctors.models import Doctor

# Create your models here.

class Appointment(models.Model):
    STATUS_CHOICES=[
        ("Scheduled", "Scheduled"),
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Confirmed", "Confirmed"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")

    appointment_date = models.DateField(db_index=True)
    appointment_time = models.TimeField()

    reason = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Scheduled", db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)

    notes = models.TextField(blank=True)

    class Meta:
        ordering = [
            "appointment_date",
            "appointment_time",
        ]

    def __str__(self):
        return f"{self.patient} - Dr. {self.doctor}"
    



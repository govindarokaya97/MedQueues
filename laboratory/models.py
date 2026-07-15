from django.db import models
from appointments.models import Appointment
from patients.models import Patient
from doctors.models import Doctor

# Create your models here.

class LabTest(models.Model):

    STATUS = [
        ("Pending", "Pending"),
        ("Sample Collected", "Sample Collected"),
        ("Processing", "Processing"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )

    test_name = models.CharField(max_length=100)

    test_fee = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pending"
    )

    requested_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.test_name





class LabReport(models.Model):

    lab_test = models.OneToOneField(
        LabTest,
        on_delete=models.CASCADE
    )

    technician = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True
    )

    result = models.TextField()

    remarks = models.TextField(blank=True)

    report_file = models.FileField(
        upload_to="lab_reports/",
        blank=True,
        null=True
    )

    completed_date = models.DateTimeField(auto_now_add=True)
from django.db import models
from appointments.models import Appointment
from patients.models import Patient
from doctors.models import Doctor
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class LabTest(models.Model):

    name = models.CharField(
        max_length=100,
        null = True
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        null = True
    )
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    normal_range = models.CharField(max_length=200, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering =["name"]

    def __str__(self):
        return f"{self.code} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = f"LAB-{self.id or 'NEW'}"
        super().save(*args, **kwargs)




class LabReport(models.Model):

    REPORT_STATUS = (
        ("Draft", "Draft"),
        ("Completed", "Completed"),
        ("Verified", "Verified"),
    )

    lab_request = models.OneToOneField(
        "LabRequest",
        on_delete=models.CASCADE,
        related_name="report",
    )

    technician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="prepared_lab_reports"
    )

    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_lab_reports"
    )

    report_summary = models.TextField(
        blank=True,
        help_text="Overall findings and diagnosis."
    )

    remarks = models.TextField(blank=True)

    report_file = models.FileField(
        upload_to="lab_reports/pdf/",
        blank=True,
        null=True
    )

    report_image = models.ImageField(
        upload_to="lab_reports/images/",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=REPORT_STATUS,
        default="Draft"
    )

    generated_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    verified_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["-generated_at"]
        verbose_name = "Laboratory Report"
        verbose_name_plural = "Laboratory Reports"

    def __str__(self):
        return (
            f"Lab Report #{self.id} - "
            f"{self.lab_request.patient}"
        )
    
    @property
    def is_verified(self):
        return self.status == "Verified"
    
    
    
class LabRequest(models.Model):
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
        on_delete=models.CASCADE,
        related_name="lab_requests"
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_lab_requests"
    )
    
    status = models.CharField(
            max_length=20,
            choices=STATUS,
            default="Pending"
    )
    
    notes = models.TextField(blank=True)
    
    requested_date = models.DateTimeField(
            auto_now_add=True
        )
    
    def __str__(self):
            return f"Lab Request#{self.id}"
    
    class Meta:
        ordering = ["-requested_date"]
        
        
        
class LabRequestItem(models.Model):
    lab_request = models.ForeignKey(
        LabRequest,
        on_delete=models.CASCADE,
        related_name="items"
    )
    
    lab_test = models.ForeignKey(
        LabTest,
        on_delete=models.CASCADE
    )
    
    
    remarks = models.CharField(
        max_length=200,
        blank=True
    )
    
    def __str__(self):
        return self.lab_test.name
    
    
    
    
    
    
    
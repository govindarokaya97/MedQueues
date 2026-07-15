from django.db import models
from appointments.models import Appointment

# Create your models here.

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    quantity = models.PositiveIntegerField()

    expiry_date = models.DateField()

    reorder_level = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.name
    
# Prescription

class Prescription(models.Model):
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE
    )

    doctor = models.ForeignKey(
        "doctors.Doctor",
        on_delete=models.CASCADE
    )

    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add= True)



# Prescription Items

class PrescriptionItems(models.Model):
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name="items"
    )

    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE
    )

    dosage = models.CharField(max_length=100)

    duration = models.CharField(max_length=100)

    quantity = models.PositiveIntegerField()

    instructions = models.TextField(blank=True)















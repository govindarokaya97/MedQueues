from django.db import models
from appointments.models import Appointment
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()
class MedicineCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Medicine Category"
        verbose_name_plural = "Medicine Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Medicine(models.Model):
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200)
    category = models.ForeignKey(
        MedicineCategory,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    manufacturer = models.CharField(max_length=100)
    batch_number = models.CharField(max_length=200, blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    stock_quantity = models.PositiveIntegerField(default=0)
    
    minimum_stock = models.PositiveIntegerField(default=10)
    reorder_level = models.PositiveIntegerField(default=10)

    expiry_date = models.DateField()
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["expiry_date"]),
        ]

    def __str__(self):
        return self.name

    @property
    def is_low_stock(self):
        return self.quantity <= self.reorder_level
    
    @property
    def is_expired(self):
        return self.expiry_date < timezone.now().date()


class Prescription(models.Model):
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name="prescription",
    )
    doctor = models.ForeignKey(
        "doctors.Doctor",
        on_delete=models.CASCADE,
        related_name="prescriptions",
    )
    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.CASCADE,
        related_name="prescriptions",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Prescription #{self.pk} for {self.patient}"


class PrescriptionItems(models.Model):
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name="items",
    )
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name="prescription_items",
    )

    dosage = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    instructions = models.TextField(blank=True)

    class Meta:
        verbose_name = "Prescription Item"
        verbose_name_plural = "Prescription Items"

    def __str__(self):
        return f"{self.medicine.name} ({self.dosage}) - {self.prescription}"
    
    



class StockTransaction(models.Model):
    
    STOCK_IN = "IN"
    STOCK_OUT = "OUT"
    
    TRANSACTION_TYPES = (
        ("STOCK_IN", "Stock In"),
        ("STOCK_OUT", "Stock Out")
    )
    
    medicine = models.ForeignKey(
        Medicine,
        on_delete= models.CASCADE,
        related_name="transactions"
    )
    
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )
    
    quantity = models.PositiveIntegerField()
    remarks = models.CharField(
        max_length= 100,
        blank=True
    )
    
    performed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:
            if self.transaction_type == self.STOCK_IN:
                self.medicine.stock_quantity += self.quantity
            elif self.transaction_type == self.STOCK_OUT:
                if self.medicine.stock_quantity < self.quantity:
                    raise ValidationError(
                        "Insufficient stock available."
                    )
                self.medicine.stock_quantity -= self.quantity
            self.medicine.save()
        super().save(*args, **kwargs)
        
    @property
    def stock_status(self):
        if self.quantity == 0:
            return "out"
        elif self.quantity <= self.minimum_stock:
            return "low"
        return "available"
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
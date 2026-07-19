from django.db import models
from patients.models import Patient
from appointments.models import Appointment
from django.utils import timezone
from django.conf import settings
from decimal import Decimal

class Bill(models.Model):
    PAYMENT_METHODS = [
        ("Cash", "Cash"),
        ("Card", "Card"),
        ("Khalti", "Khalti"),
        ("eSewa", "eSewa"),
        ("Bank Transfer", "Bank Transfer"),
    ]

    PAYMENT_STATUS = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Cancelled", "Cancelled"),
        ("Refunded", "Refunded"),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='bills'
    )

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name="bill"
    )

    invoice_number = models.CharField(max_length=20, unique=True)

    

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        blank=True,
        default="Cash"
    )
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='Pending')

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null= True
    )

    notes = models.TextField(blank= True)

    payment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.invoice_number
          
    @property
    def subtotal(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def grand_total(self):
        return self.subtotal + self.tax - self.discount


    def save(self,*args, **kwargs):
        if not self.invoice_number:
            today = timezone.now().strftime("%Y%m%d")
            
            last_bill = Bill.objects.filter(
                invoice_number__startswith=f"INV-{today}"
            ).count() +1
            
            self.invoice_number = f"INV-{today}-{last_bill:04d}"

        super().save(*args, **kwargs)
                

    
class BillItem(models.Model):
    bill = models.ForeignKey(
        Bill,
        on_delete=models.CASCADE,
        related_name= "items"
    )

    service_name = models.CharField(max_length= 100)

    quantity = models.PositiveIntegerField(default=1)

    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0 )
    

    SERVICE_TYPE_CHOICES = (
        ("CONSULTATION", "Consultation"),
        ("MEDICINE", "Medicine"),
        ("LABORATORY", "Laboratory"),
        ("ROOM", "Room"),
        ("OTHER", "Other"),
    )
        
    service_type = models.CharField(
        max_length=30,
        choices=SERVICE_TYPE_CHOICES,
        default="OTHER",
    )


     
    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)
                



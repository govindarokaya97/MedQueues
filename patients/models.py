from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from accounts.models import CustomUser

# Create your models here.
class Patient(models.Model):
    user = models.OneToOneField(
    CustomUser,
    on_delete=models.CASCADE,
    related_name="patient"
    )

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]


    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=5)

    phone = models.CharField(max_length=15)
    address = models.TextField()

    disease = models.CharField(max_length=250)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone = models.CharField(
        max_length=15,
        null=True,
        blank=True,
    )

    relationship = models.CharField(
        max_length=50,
        default=""
    )
    emergency_contact_address = models.TextField(blank=True, null=True)



    profile_photo = models.ImageField(
        upload_to="patients/",
        blank=True,
        null=True
    )

    medical_history = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    chronic_disease = models.CharField( max_length=200, blank=True)

    height = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        null=True,
        blank=True
    )

    weight = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.get_full_name()
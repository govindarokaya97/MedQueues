from django.db import models
from django.conf import settings

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    experience = models.PositiveIntegerField(help_text="Years of experience")
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)

    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True)

    available = models.BooleanField(default=True)

    joined_date = models.DateField(auto_now_add=True)

    profile_photo = models.ImageField(
        upload_to='doctor_photos/', 
        blank=True, 
        null=True)
    

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} or {self.user.username}"


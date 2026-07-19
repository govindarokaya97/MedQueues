from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="doctor"
    )
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    experience = models.PositiveIntegerField(help_text="Years of experience")
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)

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



class DoctorSchedule(models.Model):
    Days = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    ]

    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE, related_name="schedules")

    day = models.CharField(max_length=10, choices=Days)
    start_time = models.TimeField()
    end_time = models.TimeField()

    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ["doctor", "day", "start_time"]

    def __str__(self):
        return f"{self.doctor} - {self.day} {self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')}"

    def clean(self):
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time.")

        if self.doctor_id and self.day:
            overlapping = DoctorSchedule.objects.filter(
                doctor_id=self.doctor_id,
                day=self.day,
            ).exclude(id=self.id)
            for slot in overlapping:
                if self.start_time < slot.end_time and slot.start_time < self.end_time:
                    raise ValidationError(
                        f"This slot overlaps with an existing slot "
                        f"({slot.start_time.strftime('%H:%M')}-{slot.end_time.strftime('%H:%M')}) on {self.day}."
                    )


class DoctorLeave(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="leaves")
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")

    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="reviewed_leaves"
    )

    class Meta:
        ordering = ["-requested_at"]

    def __str__(self):
        return f"{self.doctor} leave {self.start_date} to {self.end_date} ({self.status})"

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Start date must be on or before end date.")
from django.db import models, transaction
from django.db.models import Max
from django.utils import timezone
from patients.models import Patient
from doctors.models import Doctor

# Create your models here.

class Appointment(models.Model):
    STATUS_CHOICES=[
        ("Scheduled", "Scheduled"),
        ("Pending", "Pending"),
        ("Waiting", "Waiting"),
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

    # --- Live queue / token fields ---
    queue_number = models.PositiveIntegerField(null=True, blank=True)
    checked_in_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = [
            "appointment_date",
            "appointment_time",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "appointment_date", "queue_number"],
                name="unique_doctor_daily_queue_number",
            ),
        ]

    def __str__(self):
        return f"{self.patient} - Dr. {self.doctor}"

    def check_in(self):
        """Assign the next queue token for this doctor/date and mark as Waiting."""
        if self.queue_number is not None:
            return

        # Lock the day's queue while allocating the token so two check-ins
        # cannot be given the same number.
        with transaction.atomic():
            Appointment.objects.select_for_update().filter(
                doctor=self.doctor,
                appointment_date=self.appointment_date,
            ).exists()
            last_number = Appointment.objects.filter(
                doctor=self.doctor,
                appointment_date=self.appointment_date,
            ).aggregate(last_number=Max("queue_number"))["last_number"]
            self.queue_number = (last_number or 0) + 1
            self.checked_in_at = timezone.now()
            self.status = "Waiting"
            self.save(update_fields=["queue_number", "checked_in_at", "status"])

    @property
    def queue_position(self):
        """1-based position in today's waiting line for this doctor (None if not waiting)."""
        if self.status != "Waiting" or self.queue_number is None:
            return None
        ahead = Appointment.objects.filter(
            doctor=self.doctor,
            appointment_date=self.appointment_date,
            status="Waiting",
            queue_number__lt=self.queue_number,
        ).count()
        return ahead + 1

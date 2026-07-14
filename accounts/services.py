from django.db import transaction
from .models import CustomUser
from .utils import generate_username


def create_doctor_account(doctor_form):
    with transaction.atomic():

        username = generate_username("DR")

        user = CustomUser.objects.create_user(
            username=username,
            password="doctor123",
            role="doctor",
            first_name=doctor_form.cleaned_data["first_name"],
            last_name=doctor_form.cleaned_data["last_name"],
            email=doctor_form.cleaned_data["email"],
        )

        doctor = doctor_form.save(commit=False)
        doctor.user = user
        doctor.save()

        return doctor, user
from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "get_full_name",
        "gender",
        "phone",
        "blood_group",
        "created_at",
    )

    search_fields = (
        "user__first_name",
        "user__last_name",
        "phone",
    )

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    get_full_name.short_description = "Patient Name"
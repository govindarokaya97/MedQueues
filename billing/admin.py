from django.contrib import admin
from .models import Bill

# Register your models here.

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_number',
        'patient',
        'total_amount',
        'payment_status',
        'payment_method',
        'created_at',
    )

    search_felds = (
        'invoice_number',
        'patient__first_name',
    )

    list_filter = (
        'payment_status',
        'payment_method'
    )



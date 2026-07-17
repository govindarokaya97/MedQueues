from django.contrib import admin
from .models import Medicine, MedicineCategory

# Register your models here.

@admin.register(MedicineCategory)
class MedicineCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    
@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "manufacturer",
        "stock_quantity",
        "price",
        "expiry_date",
    )

    list_filter = (
        "category",
        "expiry_date",
    )
    
    search_fields = [
        "name",
        "generic_name",
        "batch_number",
    ]
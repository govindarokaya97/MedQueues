from django.contrib import admin
from .models import Doctor, Department, DoctorSchedule

# Register your models here.

# @admin.register(Department)
# class DepartmentAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)


# @admin.register(Doctor)
# class DoctorAdmin(admin.ModelAdmin):
#     list_display = ('user', 'department', 'specialization', 'experience', 'available')
#     list_filter = ('department', 'available')
#     search_fields = ('user__username', 'user__first_name', 'user__last_name', 'specialization')


admin.site.register(Department)
admin.site.register(Doctor)
admin.site.register(DoctorSchedule)



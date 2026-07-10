from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/",views.appointment_dashboard, name="appointments_dashboard" ),
    path("", views.appointment_list, name="appointments_list"),
    path("add/", views.appointment_create, name="appointments_add"),

    path("upcoming/", views.upcoming_appointments, name="upcoming_appointments"),
    path("report/", views.appointment_report, name="appointments_report"),


    path("<int:id>/", views.appointment_detail, name="appointments_detail"),
    path("<int:id>/edit/", views.appointment_update, name="appointments_edit"),
    path("<int:id>/delete/", views.appointment_delete, name="appointments_delete"),
    path("<int:id>/slip/", views.appointment_slip, name="appointments_slip"),
]

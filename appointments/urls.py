from django.urls import path
from . import views
from pharmacy.views import prescription_create

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
    path("<int:id>/check-in/", views.appointment_check_in, name="appointments_check_in"),

    path("queue/my-status/", views.my_queue_status, name="my_queue_status"),
    path("queue/<int:doctor_id>/", views.queue_board, name="queue_board"),
    path("queue/<int:doctor_id>/data/", views.queue_board_data, name="queue_board_data"),
    path("queue/<int:doctor_id>/call-next/", views.call_next_patient, name="queue_call_next"),

    path("appointments/<int:appointment_id>/prescription/", prescription_create, name="prescription_create")
    
]

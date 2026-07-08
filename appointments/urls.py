from django.urls import path
from . import views

urlpatterns = [
    path("", views.appointment_list, name="appointments_list"),
    path("add/", views.appointment_create, name="appointments_add"),
    path("<int:id>/", views.appointment_detail, name="appointments_detail"),
    path("<int:id>/edit/", views.appointment_update, name="appointments_edit"),
    path("<int:id>/delete/", views.appointment_delete, name="appointments_delete"),

]

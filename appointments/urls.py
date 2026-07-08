from django.urls import path
from . import views

urlpatterns = [
    path("", views.appointment_list, name="appointments_list"),
    path("add/", views.appointment_create, name="appointments_add"),
]

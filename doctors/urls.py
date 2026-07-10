
from django.urls import path
from . import views

urlpatterns = [
    path("", views.doctor_list, name="doctor_list"),
    path('add/', views.doctor_create, name='doctor_add'),

    path("leaves/", views.leave_list, name="leave_list"),
    path("leaves/<int:id>/<str:action>/", views.leave_review, name="leave_review"),

    path("<int:id>/", views.doctor_detail, name="doctor_detail"),
    path("<int:id>/edit/", views.doctor_update, name="doctor_edit"),
    path("<int:id>/delete/",views.doctor_delete, name="doctor_delete"),

    path("<int:id>/schedule/", views.doctor_schedule, name="doctor_schedule"),
    path("<int:id>/schedule/<int:slot_id>/delete/", views.doctor_schedule_delete, name="doctor_schedule_delete"),

    path("<int:id>/leave/request/", views.leave_request_create, name="leave_request_create"),
]
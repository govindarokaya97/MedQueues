from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    
    path("", views.doctor_list, name="doctor_list"),
    path('add/', views.doctor_create, name='doctor_add'),

    path("<int:id>/", views.doctor_detail, name="doctor_detail"),
    path("<int:id>/edit/", views.doctor_update, name="doctor_edit"),
    path("<int:id>/delete/",views.doctor_delete, name="doctor_delete"),
]
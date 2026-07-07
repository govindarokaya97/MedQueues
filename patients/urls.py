from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_list, name='patient_list'),
    path('add/', views.patient_create, name='patient_add'),
    path('<int:id>/', views.patient_detail, name='patient_detail'),
    path('<int:id>/edit/', views.patient_update, name='patient_update'),
    path('<int:id>/delete/', views.patient_delete, name='patient_delete'),
]
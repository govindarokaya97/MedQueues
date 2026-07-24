from django.urls import path
from . import views

urlpatterns =[
    path('',views.dashboard, name='report_dashboard' ),
    path('patients/', views.patient_report , name='patient_report' ),
    path("patients/<int:id>/", views.patient_report_detail, name="patient_report_detail" ),
    
    # path("doctors/", views.doctor_report, name="doctor_report" ),
    # path("doctors/<int:id>/", views.doctors_report_detail, name="doctor_report_detail" ),
    
]
from django.urls import path 
from . import views

urlpatterns = [
    path('', views.MedicineListView.as_view(), name='medicine_list'),
    path('add/', views.MedicineCreateView.as_view(), name='medicine_add'),
        path(
        "medicine/<int:id>/",
        views.MedicineDetailView.as_view(),
        name="medicine_detail"
    ),

    path(
        "medicine/<int:medicine_id>/details/",
        views.medicine_details,
        name="medicine_details"
    ),
    path('<int:id>/edit/', views.MedicineUpdateView.as_view(), name='medicine_edit'),
    path('<int:id>/delete/', views.MedicineDeleteView.as_view(), name='medicine_delete'),
    
    path('stock/', views.StockTransactionCreativeView.as_view(), name='stock_transaction'),

    
    path(
        "prescriptions/",
        views.prescription_list,
        name="prescription_list"
    ),


    path(
        "appointments/<int:appointment_id>/prescription/",
        views.prescription_create,
        name="prescription_create"
    ),


    path(
        "prescriptions/<int:id>/",
        views.PrescriptionDetailView.as_view(),
        name="prescription_detail"
    ),


    path(
        "prescriptions/<int:id>/dispense/",
        views.prescription_dispense,
        name="prescription_dispense"
    ),
    
    
        
]

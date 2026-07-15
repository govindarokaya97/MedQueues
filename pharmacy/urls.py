from django.urls import path 
from . import views

urlpatterns = [
    path('', views.MedicineListView.as_view(), name='medicine_list'),
    path('add/', views.MedicineCreateView.as_view(), name='medicine_add'),
    path('<int:id>/', views.MedicineDetailView.as_view(), name='medicine_detail'),
    path('<int:id>/edit/', views.MedicineUpdateView.as_view(), name='medicine_edit'),
    path('<int:id>/delete/', views.MedicineDeleteView.as_view(), name='medicine_delete'),
    
    path('stock/', views.StockTransactionCreativeView.as_view(), name='stock_transaction'),
    
    path("prescriptions/", views.prescription_list,name="prescription_list"),
    path("prescriptions/add/", views.prescription_create, name="prescription_create"),
    path("prescriptions/<int:id>/dispense/", views.prescription_dispense, name="prescription_dispense")
    
]

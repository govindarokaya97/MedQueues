from django.urls import path 
from . import views

urlpatterns = [
    path('', views.BillListView.as_view(), name='bill_list'),
    path('<int:id>/', views.BillDetailView.as_view(), name='bill_detail'),
    path('<int:id>/edit/', views.BillUpdateView.as_view(), name='bill_edit'),
    path('<int:id>/delete/', views.BillDeleteView.as_view(), name='bill_delete'),
    
    path('generate/<int:appointment_id>/', views.create_bill, name='generate_bill'),
    

]

from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
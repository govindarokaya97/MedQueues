from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
]
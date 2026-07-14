from django.urls import path
from. import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('force_password_change/', views.force_password_change_view, name='force_password_change'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('driver-dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('agent-dashboard/', views.customer_dashboard, name='agent_dashboard'),
]
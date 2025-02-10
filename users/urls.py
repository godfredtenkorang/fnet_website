from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    
    path('verity_registration_otp/', views.verify_registration_otp, name='verify_registration_otp'),
    path('reset-password/', views.request_reset_otp, name='request_reset_otp'),
    path('verify-otp/', views.verify_otp_and_reset_password, name='verify_otp_and_reset_password'),
    
    path('logout/', views.logout, name='logout'),
    # Customer URLS
    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('customer-bookings/', views.customer_bookings, name='customer_bookings'),
    path('customer-schedules/', views.customer_schedules, name='customer_schedules'),
    path('customer-flights/', views.customer_flight_booking, name='customer_flight_booking'),
    
    # Driver URLS
    path('driver-dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('my-detail/', views.driver_detail, name='driver-detail'),
    path('assigned_trip/', views.driver_book, name='driver-book'),
    
    
    path('agent-dashboard/', views.customer_dashboard, name='agent_dashboard'),
]
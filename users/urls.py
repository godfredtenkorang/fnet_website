from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    
    path('verity_registration_otp/', views.verify_registration_otp, name='verify_registration_otp'),
    path('reset-password/', views.request_reset_otp, name='request_reset_otp'),
    path('verify-otp/', views.verify_otp_and_reset_password, name='verify_otp_and_reset_password'),
    
    path('logout/', views.logout, name='logout'),
    
    path('mnotify/callback/', views.mnotify_callback, name='mnotify_callback'),
    # Customer URLS
    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('customer-bookings/', views.customer_bookings, name='customer_bookings'),
    path('customer-schedules/', views.customer_schedules, name='customer_schedules'),
    path('customer-flights/', views.customer_flight_booking, name='customer_flight_booking'),
    path('customer-payment/', views.payment, name='customer-payment'),
    path('customer-payment-form/<int:rental_id>/', views.payment_detail, name='customer-payment-form'),
    path('customer-properties/', views.all_properies_bookings, name='all_properies_bookings'),
    
    # Driver URLS
    path('driver-dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('my-details/', views.driver_detail, name='driver-detail'),
    path('trips/', views.driver_trips, name='driver-trips'),
    path('assigned_trip/', views.driver_book, name='driver-book'),
    
    path('add_mileage/', views.add_mileage, name='add-mileage'),
    path('view_mileage/', views.view_mileage, name='view-mileage'),
    path('update_mileage/<int:mileage_id>/', views.update_mileage, name='update-mileage'),
    path('mileage/', views.mileage, name='mileage'),
    path('vehicle_maintenance/<int:vehicle_id>/', views.vehicle_maintenance, name='vehicle_maintenance'),
    path('record_oil_change/<int:vehicle_id>/', views.record_oil_change, name='record_oil_change'),
    
    
    path('add_fuel/', views.add_fuel, name='add-fuel'),
    path('view_fuel/', views.view_fuel, name='view-fuel'),
    path('add_expense/', views.add_expenses, name='add-expense'),
    path('view_expense/', views.view_expenses, name='view-expense'),
    
    
    path('agent-dashboard/', views.agent_dashboard, name='agent_dashboard'),
    path('agent-trips/', views.agent_trips, name='agent-trips'),
    path('my_details/', views.agent_detail, name='agent-detail'),
    path('agent_assigned_trip/', views.agent_book, name='agent-book'),
]
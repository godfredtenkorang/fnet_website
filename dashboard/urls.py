from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('contact/', views.contact, name='contact'),
    path('sendMessage/', views.sendMessage, name='sendMessage'),
    path('bookings/', views.bookings, name='bookings'),
    path('appointments/', views.appointments, name='appointments'),
    path('appointments/<int:appointment_id>/assign_driver/', views.update_appointment, name='create-appointment'),
    
    path('add_expense/', views.add_expenses, name='add_expense'),
    path('view_expenses/', views.view_expenses, name='view_expenses'),
    path('get_pdf/', views.get_pdf, name='get_pdf'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
    
    
    path('driver_list/', views.driver_list, name='driver-list'),
    path('driver/register/', views.register_driver, name='register-driver'),
    path('cars/<int:car_id>/assign_driver/', views.assign_driver, name='assign-driver'),
    
]
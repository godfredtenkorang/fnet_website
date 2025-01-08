from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('contact/', views.contact, name='contact'),
    path('sendMessage/', views.sendMessage, name='sendMessage'),
    path('bookings/', views.bookings, name='bookings'),
    path('appointments/', views.appointments, name='appointments'),
    
    path('add_expense/', views.add_expenses, name='add_expense'),
    path('view_expenses/', views.view_expenses, name='view_expenses'),
    path('get_pdf/', views.get_pdf, name='get_pdf'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
]
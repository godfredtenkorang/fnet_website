from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('contact/', views.contact, name='contact'),
    path('sendMessage/', views.sendMessage, name='sendMessage'),
    path('bookings/', views.bookings, name='bookings'),
    path('appointments/', views.appointments, name='appointments'),
]
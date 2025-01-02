from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('carDetail', views.carDetail, name='carDetail'),
    path('carDetail', views.carDetail, name='carDetail'),
    path('rentCars', views.rentCars, name='rentCars'),
    path('aboutUs', views.aboutUs, name='aboutUs'),
    path('service', views.service, name='service'),
    path('contactUs', views.contactUs, name='contactUs'),
    path('booking', views.booking, name='booking'),
    path('bookings', views.bookings, name='bookings'),
    path('signUp', views.signUp, name='signUp'),
    path('login', views.login, name='login'),
    path('termsAndCondition', views.termsAndCondition, name='termsAndCondition'),
    path('home', views.home, name='home'), 
  
]
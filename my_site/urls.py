from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('carDetail', views.carDetail, name='carDetail'),
    path('carDetail', views.carDetail, name='carDetail'),
    path('rentCars', views.rentCars, name='rentCars'),
    path('aboutUs', views.aboutUs, name='aboutUs'),
    path('service', views.service, name='service'),
    path('contactUs', views.contactUs, name='contactUs'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rent_cars/', views.rentCars, name='rentCars'),
    path('car_detail/<slug:car_slug>/', views.carDetail, name='carDetail'),
    path('about_us/', views.aboutUs, name='aboutUs'),
    path('service/', views.service, name='service'),
    path('contact_us/', views.contactUs, name='contactUs'),
    
    path('signUp/', views.signUp, name='signUp'),
    path('login/', views.login, name='login'),
    path('sucessPage/', views.sucessPage, name='sucessPage'),
    path('unsucessPage/', views.unsucessPage, name='unsucessPage'),
    path('terms_and_condition/', views.termsAndCondition, name='termsAndCondition'),
]
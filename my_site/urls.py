from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rent_cars/', views.rentCars, name='rentCars'),
    path('search/<slug:category_slug>/', views.list_category, name='list-category'),
    path('car_detail/<slug:car_slug>/', views.carDetail, name='carDetail'),
    path('about_us/', views.aboutUs, name='aboutUs'),
    path('service/', views.service, name='service'),
    path('contact_us/', views.contactUs, name='contactUs'),
    
    path('signUp/', views.signUp, name='signUp'),
    path('sucessPage/', views.sucessPage, name='sucessPage'),
    path('unsucessPage/', views.unsucessPage, name='unsucessPage'),
    path('success_page/', views.contact_success_page, name='contact-success'),
    path('terms_and_condition/', views.termsAndCondition, name='termsAndCondition'),
    path('gallery/', views.gallery, name='gallery'),
    
    path('review/<int:driver_id>/', views.review_driver, name='review_driver'),
    path('thank_you/', views.thank_you_page, name='thank_you_page'),

]
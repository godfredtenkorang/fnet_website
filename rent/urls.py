from django.urls import path
from . import views


urlpatterns = [
    path('house/', views.rent_house, name='rent-house'),
    path('house-detail/<slug:rent_slug>/', views.rent_detail, name='rent-detail'),
    path('house-booking/<slug:rent_slug>/', views.rent_booking, name='rent-booking'),
]
from django.urls import path
from . import views


urlpatterns = [
    path('flight-list/', views.flight, name='flight-list'),
    path('flight-booking/<slug:flight_slug>/', views.booking, name='booking'),
]
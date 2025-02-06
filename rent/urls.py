from django.urls import path
from . import views


urlpatterns = [
    path('house/', views.rent_house, name='rent-house')
]
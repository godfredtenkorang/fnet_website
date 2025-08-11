from django.urls import path
from . import views


urlpatterns = [
    path('owner_dashboard/', views.dashboard, name='owner_dashboard')
]
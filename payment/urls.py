from django.urls import path
from . import views

urlpatterns = [
    path('make_payment/', views.payment, name='make_payment'),
]
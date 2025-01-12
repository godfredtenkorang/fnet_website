from django.urls import path
from . import views


urlpatterns = [
    path('appointment/', views.appointment, name='appointment'),
    path('bookings/<slug:car_slug>/payment/', views.process_payment, name='process-payment'),
    path('sucess-page/', views.sucessPage, name='sucess-page'),
    path('unsucess-page/', views.unsucessPage, name='unsucess-page'),
]
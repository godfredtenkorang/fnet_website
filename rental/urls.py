from django.urls import path
from . import views


urlpatterns = [
    path('schedule-cars/', views.all_schedule_cars, name='all_schedule_cars'),
    path('schedule-a-ride/<int:car_id>/book_now/', views.schedule_a_ride, name='appointment'),
    path('bookings/<slug:car_slug>/payment/', views.process_payment, name='process-payment'),
    path('sucess-page/', views.sucessPage, name='sucess-page'),
    path('unsucess-page/', views.unsucessPage, name='unsucess-page'),
]
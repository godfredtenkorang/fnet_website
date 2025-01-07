from django.urls import path
from . import views


urlpatterns = [
    path('appointment/', views.appointment, name='appointment'),
    path('sucess-page/', views.sucessPage, name='sucess-page'),
    path('unsucess-page/', views.unsucessPage, name='unsucess-page'),
]
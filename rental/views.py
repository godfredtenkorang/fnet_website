from django.shortcuts import render
from .models import Appointment


def appointment(request):
    return render(request, 'rental/appointment.html')

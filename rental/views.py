from django.shortcuts import render, redirect
from .models import Appointment


def appointment(request):
    if request.method == 'POST':
        customer_name = request.POST['customer_name']
        customer_email = request.POST['customer_email']
        customer_phone = request.POST['customer_phone']
        appointment_date = request.POST['appointment_date']
        appointment_time = request.POST['appointment_time']
        purpose = request.POST['purpose']
        
        appointments = Appointment(customer_name=customer_name, customer_email=customer_email, customer_phone=customer_phone, appointment_date=appointment_date, appointment_time=appointment_time, purpose=purpose)
        appointments.save()
        return redirect('appointment')
    
    context = {
        'title': 'Appointment'
    }
    return render(request, 'rental/appointment.html')

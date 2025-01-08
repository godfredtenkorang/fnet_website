from django.shortcuts import render, redirect
from .models import Appointment
from django.conf import settings
from django.core.mail import send_mail
from .utils import send_sms, receive_sms

def appointment(request):
    if request.method == 'POST':
        customer_name = request.POST['customer_name']
        customer_email = request.POST['customer_email']
        customer_phone = request.POST['customer_phone']
        appointment_date = request.POST['appointment_date']
        appointment_time = request.POST['appointment_time']
        pick_up_location = request.POST['pick_up_location']
        drop_off_location = request.POST['drop_off_location']
        gps_address = request.POST['gps_address']
        purpose = request.POST['purpose']
        
        appointments = Appointment(customer_name=customer_name, customer_email=customer_email, customer_phone=customer_phone, appointment_date=appointment_date, appointment_time=appointment_time, pick_up_location=pick_up_location, drop_off_location=drop_off_location, gps_address=gps_address, purpose=purpose)
        appointments.save()
        
        # send_mail(
        #     'Booking Confirmation',
        #     f'Thank you for booking {car.car_name}. Your booking details are as follows:\n\n'
        #     f'Customer Name: {customer_name}\n'
        #     f'Car: {car.car_name}\n'
        #     f'Rental Date: {rental_date}\n'
        #     f'Return Date: {return_date}\n'
        #     f'Total Price: ${total_price}',
        # )
        send_sms(customer_phone, customer_name, appointment_date, appointment_time, purpose)
        receive_sms(customer_name, customer_phone, appointment_date, appointment_time, purpose)
        
        return redirect('sucess-page')
    
    context = {
        'title': 'Appointment'
    }
    return render(request, 'rental/appointment.html', context)


def sucessPage(request):
    return render(request, 'rental/sucessPage.html')

def unsucessPage(request):
    return render(request, 'rental/unsucessPage.html')

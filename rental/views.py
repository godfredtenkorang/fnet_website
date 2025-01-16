from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment, Payment
from django.conf import settings
from django.core.mail import send_mail
from .utils import send_sms, receive_sms, payment_send_sms, receive_payment_sms
from my_site.models import Car
from .forms import PaymentForm

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
        
        appointments = Appointment( customer_name=customer_name, customer_email=customer_email, customer_phone=customer_phone, appointment_date=appointment_date, appointment_time=appointment_time, pick_up_location=pick_up_location, drop_off_location=drop_off_location, gps_address=gps_address, purpose=purpose)
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


def process_payment(request, car_slug):
    car = get_object_or_404(Car, slug=car_slug)
    
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone')
        rental_date = request.POST.get('rental_date')
        return_date = request.POST.get('return_date')
        pick_up_location = request.POST.get('pick_up_location')
        drop_off_location = request.POST.get('drop_off_location')
        payment_method = request.POST.get('payment_method')
        momo_code = request.POST.get('momo_code')
        transaction_id = request.POST.get('transaction_id')
        
        from datetime import datetime

        rental_date = datetime.strptime(rental_date, '%Y-%m-%d').date()
        return_date = datetime.strptime(return_date, '%Y-%m-%d').date()

        # Calculate total price based on rental days
        rental_days = (return_date - rental_date).days
        total_price = rental_days * car.price_per_day if rental_days > 0 else 0
        
        payments = Payment(car=car, customer_name=customer_name, customer_email=customer_email, customer_phone=customer_phone, rental_date=rental_date, return_date=return_date, pick_up_location=pick_up_location, drop_off_location=drop_off_location, payment_method=payment_method, momo_code=momo_code, transaction_id=transaction_id, total_price=total_price)
        payments.car = car
        payments.is_successful = True
        payments.save()
        
        payment_send_sms(customer_phone, customer_name, car.car_name, rental_date, return_date, pick_up_location, drop_off_location, transaction_id, total_price)
        receive_payment_sms(customer_name, customer_phone, car.car_name, rental_date, return_date, pick_up_location, drop_off_location, transaction_id, total_price)
        
        return redirect('index')
    

    
    return render(request, 'rental/booking.html', {'car': car})

def sucessPage(request):
    return render(request, 'rental/sucessPage.html')

def unsucessPage(request):
    return render(request, 'rental/unsucessPage.html')

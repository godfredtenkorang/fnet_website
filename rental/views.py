from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment, Payment, Region
from django.conf import settings
from django.core.mail import send_mail
from .utils import send_sms, receive_sms, payment_send_sms, receive_payment_sms
from my_site.models import Car
from .forms import PaymentForm
from django.utils.timezone import datetime
from decimal import Decimal
from django.contrib import messages
from my_site.utils import get_location_based_price


def all_schedule_cars(request):
    category = request.GET.get('category', 'Scheduled Drive')
    schedule_cars = Car.objects.filter(category__name=category)
    
    context = {
        'schedule_cars': schedule_cars,
        'title': 'Scheduled Cars'
    }
    
    return render(request, 'rental/schedule_cars.html', context)

def schedule_a_ride(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        schedule_date = request.POST.get('schedule_date')
        pick_up_time = request.POST.get('pick_up_time')
        drop_off_time = request.POST.get('drop_off_time')
        pick_up_location = request.POST.get('pick_up_location')
        drop_off_location = request.POST.get('drop_off_location')
        gps_address = request.POST.get('gps_address')
        purpose = request.POST.get('purpose')
        
        # Parse pick-up and drop-off times
        pick_up_time = datetime.strptime(pick_up_time, '%H:%M')
        drop_off_time = datetime.strptime(drop_off_time, '%H:%M')
        
        if drop_off_time <= pick_up_time:
            messages.error(request, "Drop-off time must be after pick-up time.")
            return redirect('index')
        
        # Calculate the duration and total price
        duration = (drop_off_time - pick_up_time).total_seconds() / 3600
        duration_decimal = Decimal(duration)
        total_price = car.price_per_hour * duration_decimal
        
        appointments = Appointment(car=car, customer_name=customer_name, customer_phone=customer_phone, schedule_date=schedule_date, pick_up_time=pick_up_time, drop_off_time=drop_off_time, pick_up_location=pick_up_location, drop_off_location=drop_off_location, gps_address=gps_address, purpose=purpose, total_price=total_price)
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
        send_sms(customer_phone, customer_name, schedule_date, pick_up_time, purpose)
        receive_sms(customer_name, customer_phone, schedule_date, pick_up_time, purpose)
        
        return redirect('sucess-page')
    
    context = {
        
        'title': 'Appointment'
    }
    return render(request, 'rental/appointment.html', context)


def process_payment(request, car_slug):
    car = get_object_or_404(Car, slug=car_slug)
    
    regions = Region.objects.all()
    
    if request.method == 'POST':
        region_id = request.POST.get('region')
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        rental_date = request.POST.get('rental_date')
        return_date = request.POST.get('return_date')
        location_category = request.POST.get('location_category')
        town = request.POST.get('town')
        pick_up_time = request.POST.get('pick_up_time')
        drop_off_time = request.POST.get('drop_off_time')
        pick_up_location = request.POST.get('pick_up_location')
        drop_off_location = request.POST.get('drop_off_location')
        document_type = request.POST.get('document_type')
        document_number = request.POST.get('document_number')
        payment_method = request.POST.get('payment_method')
        momo_code = request.POST.get('momo_code')
        transaction_id = request.POST.get('transaction_id')
        
        region = get_object_or_404(Region, id=region_id)
        daily_price = get_location_based_price(car, location_category)
        
        from datetime import datetime

        rental_date = datetime.strptime(rental_date, '%Y-%m-%d').date()
        return_date = datetime.strptime(return_date, '%Y-%m-%d').date()

        # Calculate total price based on rental days
        rental_days = (return_date - rental_date).days
        total_price = rental_days * daily_price if rental_days > 0 else 0
        
        payments = Payment(car=car, customer_name=customer_name, customer_phone=customer_phone, rental_date=rental_date, return_date=return_date, region=region, town=town, location_category=location_category, pick_up_time=pick_up_time, drop_off_time=drop_off_time, pick_up_location=pick_up_location, drop_off_location=drop_off_location, document_type=document_type, document_number=document_number, payment_method=payment_method, momo_code=momo_code, transaction_id=transaction_id, total_price=total_price)
        payments.car = car
        payments.is_successful = True
        payments.save()
        
        payment_send_sms(customer_phone, customer_name, car.car_name, rental_date, return_date, pick_up_location, drop_off_location, transaction_id, total_price)
        receive_payment_sms(customer_name, customer_phone, car.car_name, rental_date, return_date, pick_up_location, drop_off_location, transaction_id, total_price)
        
        return redirect('index')
    

    
    return render(request, 'rental/booking.html', {'car': car, 'regions': regions})

def sucessPage(request):
    return render(request, 'rental/sucessPage.html')

def unsucessPage(request):
    return render(request, 'rental/unsucessPage.html')

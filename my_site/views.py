from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, Category, Gallery, Driver, DriverReview
from rental.models import Rental, Contact
from django.conf import settings
from django.core.mail import send_mail
from .utils import send_sms, receive_sms, receive_contact, get_location_based_price
from django.http import JsonResponse
from dashboard.models import Customer
import random
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    # cars = list(Car.objects.filter(availability_status='Available'))
    cars = list(Car.objects.all())
    random.shuffle(cars)
    random_cars = cars[:8]
    return render(request, 'my_site/index.html', {'cars': random_cars})


def rentCars(request):
    
    cars = list(Car.objects.all())
    random.shuffle(cars)
    random_cars = cars
    
    context = {
        'cars': random_cars,
        'title': 'Cars'
    }
    return render(request, 'my_site/rentCars.html', context)

def list_category(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    cars = list(Car.objects.filter(category=category))
    random.shuffle(cars)
    random_cars = cars
    
    context = {
        'category': category,
        'cars': random_cars,
        'title': 'Categories'
    }
    return render(request, 'my_site/list_category.html', context)

def categories(request):
    all_categories = Category.objects.exclude(name="Scheduled Drive")
    return {'all_categories': all_categories}

def carDetail(request,  car_slug):
    car = get_object_or_404(Car, slug=car_slug)
    user = request.user
    
    
    if request.method == 'POST':
        
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        emergency_name = request.POST.get('emergency_name')
        emergency_phone = request.POST.get('emergency_phone')
        pick_up_time = request.POST.get('pick_up_time')
        drop_off_time = request.POST.get('drop_off_time')
        number_of_days = request.POST.get('number_of_days')
        rental_date = request.POST.get('rental_date')
        return_date = request.POST.get('return_date')
        location_category = request.POST.get('location_category')
        city = request.POST.get('city')
        town = request.POST.get('town')
        document_type = request.POST.get('document_type')
        document_number = request.POST.get('document_number')
        
        
        
        daily_price = get_location_based_price(car, location_category)
        
        from datetime import datetime

        rental_date = datetime.strptime(rental_date, '%Y-%m-%d').date()
        return_date = datetime.strptime(return_date, '%Y-%m-%d').date()
        
  

        # Calculate total price based on rental days
        # if rental_date == return_date:
        #     rental_days = 1
        # else:
        #     rental_days = (return_date - rental_date).total_seconds() / (12 * 3600)
        #     rental_days = max(1, int(rental_days))
        # Handle case where price is stored as a range "200 - 300"
        
        number_of_days = int(number_of_days)
        
        if isinstance(daily_price, str) and " - " in daily_price:
            # Split the range and convert to float instead of int
            min_price, max_price = map(float, daily_price.split(" - "))
            total_min_price = min_price * number_of_days
            total_max_price = max_price * number_of_days
            total_price = f"{total_min_price:.2f} - {total_max_price:.2f}"  # Keep two decimal places
            
        else:

            total_price = float(daily_price) * number_of_days
            
    
        
        rentals = Rental(customer=user, car=car, customer_name=customer_name, customer_phone=customer_phone, emergency_name=emergency_name, emergency_phone=emergency_phone, city=city, town=town, location_category=location_category, pick_up_time=pick_up_time, drop_off_time=drop_off_time, number_of_days=number_of_days, rental_date=rental_date, return_date=return_date, document_type=document_type, document_number=document_number, total_price=total_price)
        rentals.save()
        
        # send_mail(
        #     'Booking Confirmation',
        #     f'Thank you for booking {car.car_name}. Your booking details are as follows:\n\n'
        #     f'Customer Name: {customer_name}\n'
        #     f'Car: {car.car_name}\n'
        #     f'Rental Date: {rental_date}\n'
        #     f'Return Date: {return_date}\n'
        #     f'Total Price: ${total_price}',
        #     settings.EMAIL_HOST_USER,
        #     [customer_email],
        #     fail_silently=False,
        # )
        
        send_sms(customer_phone, customer_name, car.car_name)
        receive_sms(customer_name, customer_phone, car.car_name, rental_date, return_date, location_category, town, pick_up_time, drop_off_time, total_price)
        
        return redirect('sucessPage')
    
    context = {
        'car':car,
        'title': 'Car Detail',
    }
    return render(request, 'my_site/carDetail.html', context)


def aboutUs(request):
    context = {
        'title': 'About Us'
    }
    return render(request, 'my_site/aboutUs.html', context)

def service(request):
    context = {
        'title': 'Services'
    }
    return render(request, 'my_site/service.html', context)

def contactUs(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        contacts = Contact(name=name, email=email, phone=phone, message=message)
        contacts.save()
        # receive_contact(name, email, phone, message)
        return redirect('contact-success')
    
    context = {
        'title': 'Contact Us'
    }
    return render(request, 'my_site/contactUs.html', context)


def signUp(request):
    return render(request, 'my_site/signUp.html')

def termsAndCondition(request):
    context = {
        'title': 'T&C'
    }
    return render(request, 'my_site/termsAndCondition.html', context)

def sucessPage(request):
    return render(request, 'my_site/sucessPage.html')

def unsucessPage(request):
    return render(request, 'my_site/unsucessPage.html')

def contact_success_page(request):
    return render(request, 'my_site/contact_success.html')

def custom_404_view(request, exception):
    context = {
        'title': '404'
    }
    return render(request, 'my_site/404.html', status=404, context=context)

def gallery(request):
    galleries = Gallery.objects.all()
    context = {
        'galleries': galleries,
        'title': 'Gallery'
    }
    return render(request, 'my_site/gallery.html', context)

@login_required
def review_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    
    if request.method == "POST":
        rating = int(request.POST.get("rating"))
        review_text = request.POST.get("review_text")
        customer = request.user
        
        DriverReview.objects.create(
            driver=driver,
            customer=customer,
            rating=rating,
            review_text=review_text
        )
        
        return redirect("thank_you_page")
    
    context = {
        'driver': driver,
        'title': 'Review'
    }
    
    return render(request, "my_site/review_form.html", context)

def thank_you_page(request):

    return render(request, 'my_site/thank_you_page.html')

def AirBnBDetail(request):
    return render(request, 'my_site/AirBnBDetail.html')

def AirBnB(request):
    return render(request, 'my_site/AirBnB.html')



from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, Category
from rental.models import Rental, Contact, Region
from django.conf import settings
from django.core.mail import send_mail
from .utils import send_sms, receive_sms, receive_contact, get_location_based_price
from django.http import JsonResponse
from dashboard.models import Customer

# Create your views here.
def index(request):
    cars = Car.objects.filter(availability_status='Available')[:8]
    return render(request, 'my_site/index.html', {'cars': cars})


def rentCars(request):
    
    cars = Car.objects.all()
    
    context = {
        'cars': cars,
        'title': 'Cars'
    }
    return render(request, 'my_site/rentCars.html', context)

def list_category(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    cars = Car.objects.filter(category=category)
    
    context = {
        'category': category,
        'cars': cars,
        'title': 'Categories'
    }
    return render(request, 'my_site/list_category.html', context)

def categories(request):
    all_categories = Category.objects.all()
    return {'all_categories': all_categories}

def carDetail(request,  car_slug):
    car = get_object_or_404(Car, slug=car_slug)
    
    regions = Region.objects.all()
    
    if request.method == 'POST':
        region_id = request.POST.get('region')
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        pick_up_time = request.POST.get('pick_up_time')
        drop_off_time = request.POST.get('drop_off_time')
        rental_date = request.POST.get('rental_date')
        return_date = request.POST.get('return_date')
        location_category = request.POST.get('location_category')
        city = request.POST.get('city')
        town = request.POST.get('town')
        document_type = request.POST.get('document_type')
        document_number = request.POST.get('document_number')
        
        region = get_object_or_404(Region, id=region_id)
        daily_price = get_location_based_price(car, location_category)
        
        from datetime import datetime

        rental_date = datetime.strptime(rental_date, '%Y-%m-%d').date()
        return_date = datetime.strptime(return_date, '%Y-%m-%d').date()

        # Calculate total price based on rental days
        rental_days = (return_date - rental_date).days
        total_price = rental_days * daily_price if rental_days > 0 else 0
        
        customer, created = Customer.objects.get_or_create(
                name=customer_name,
                phone_number=customer_phone
            )
        
        rentals = Rental(car=car, customer_name=customer_name, customer_phone=customer_phone, region=region, city=city, town=town, location_category=location_category, pick_up_time=pick_up_time, drop_off_time=drop_off_time, rental_date=rental_date, return_date=return_date, document_type=document_type, document_number=document_number, total_price=total_price)
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
        
        send_sms(customer_phone, customer_name, car.car_name, rental_date, return_date, region, location_category, town, pick_up_time, drop_off_time, total_price)
        receive_sms(customer_name, customer_phone, car.car_name, rental_date, return_date, region, location_category, town, pick_up_time, drop_off_time, total_price)
        
        return redirect('sucessPage')
    
    context = {
        'car':car,
        'regions': regions,
        'title': 'Car Detail'
    }
    return render(request, 'my_site/carDetail.html', context)


def aboutUs(request):
    return render(request, 'my_site/aboutUs.html')

def service(request):
    return render(request, 'my_site/service.html')

def contactUs(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        contacts = Contact(name=name, email=email, phone=phone, message=message)
        contacts.save()
        receive_contact(name, email, phone, message)
        return redirect('contact-success')
    
    
    return render(request, 'my_site/contactUs.html')


def signUp(request):
    return render(request, 'my_site/signUp.html')

def termsAndCondition(request):
    return render(request, 'my_site/termsAndCondition.html')

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


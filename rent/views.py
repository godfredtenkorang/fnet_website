from django.shortcuts import render, get_object_or_404, redirect
from .models import Property, PropertyBooking
from .utils import property_sms, receive_property_sms
from django.contrib.auth.decorators import login_required

# Create your views here.
def rent_house(request):
    properties = Property.objects.all()
    context = {
        'properties': properties,
        'title': 'Properties'
    }
    return render(request, 'rent/rent_house.html', context)

def rent_detail(request, rent_slug):
    rent = get_object_or_404(Property, slug=rent_slug)
    context = {
        'rent': rent, 
        'title': 'Property Detail'
    }
    return render(request, 'rent/AirBnBDetail.html', context)

@login_required
def rent_booking(request, rent_slug):
    rent = get_object_or_404(Property, slug=rent_slug)
    user = request.user
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        check_in_date = request.POST['check_in_date']
        check_in_time = request.POST['check_in_time']
        check_out_date = request.POST['check_out_date']
        
        properties = PropertyBooking(user=user, property=rent, name=name, phone=phone, check_in_date=check_in_date, check_in_time=check_in_time, check_out_date=check_out_date)
        properties.save()
        
        property_sms(phone_number=phone, name=name, property_name=rent)
        receive_property_sms(name, phone, rent, check_in_date, check_in_time, check_out_date)
        
        return redirect('rent-house')
    
    context = {
        'rent': rent,
        'title': 'Property Booking'
    }
    return render(request, 'rent/AirBnBbooking.html', context)

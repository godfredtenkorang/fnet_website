from django.shortcuts import render, get_object_or_404, redirect
from .models import Airline, Booking
from .utils import send_sms, receive_sms

# Create your views here.
def flight(request):
    airlines = Airline.objects.all()
    context = {
        'airlines': airlines,
        'title': 'Flight'
    }
    return render(request, 'flight/flight_list.html', context)


def booking(request, flight_slug):
    airline = get_object_or_404(Airline, slug=flight_slug)
    user = request.user
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        category = request.POST.get('category')
        trip_from = request.POST.get('trip_from')
        trip_to = request.POST.get('trip_to')
        trip_departure = request.POST.get('trip_departure')
        trip_return = request.POST.get('trip_return')
        number_of_adults = request.POST.get('number_of_adults')
        number_of_children = request.POST.get('number_of_children')
        number_of_infants = request.POST.get('number_of_infants')

        bookings = Booking(customer=user, airline=airline, full_name=full_name, category=category, phone_number=phone_number, trip_from=trip_from, trip_to=trip_to, trip_departure=trip_departure, trip_return=trip_return, number_of_adults=number_of_adults, number_of_children=number_of_children, number_of_infants=number_of_infants)
        bookings.save()
        send_sms(phone_number, full_name, airline.name)
        receive_sms(full_name, phone_number, category, airline.name, trip_from, trip_to, trip_departure, trip_return, number_of_adults, number_of_children, number_of_infants)
        return redirect('flight-list')
    
    context = {
        'airline': airline,
        'title': 'Booking'
    }
    return render(request, 'flight/flight_booking.html', context)



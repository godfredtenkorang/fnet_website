from django.shortcuts import render
from rental.models import Contact, Rental, Appointment
from my_site.models import Car

# Create your views here.
def dashboard(request):
    cars_available = Car.objects.count()
    bookings_id = Rental.objects.count()
    return render(request, 'dashboard/dashboard.html', {'cars_available': cars_available, 'bookings_id':bookings_id})

def contact(request):
    contacts = Contact.objects.all()
    return render(request, 'dashboard/contact.html', {'contacts': contacts})

def sendMessage(request):
    return render(request, 'dashboard/sendMessage.html')

def bookings(request):
    rentals = Rental.objects.all()
    return render(request, 'dashboard/bookings.html', {'rentals': rentals})

def appointments(request):
    all_appointments = Appointment.objects.all()
    return render(request, 'dashboard/appointments.html', {'all_appointments': all_appointments})
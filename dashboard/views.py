from django.shortcuts import render
from rental.models import Contact, Rental, Appointment
from my_site.models import Car
from .utils import send_sms
from .models import SMSLog
from django.http import JsonResponse

# Create your views here.
def dashboard(request):
    cars_available = Car.objects.count()
    bookings_id = Rental.objects.count()
    return render(request, 'dashboard/dashboard.html', {'cars_available': cars_available, 'bookings_id':bookings_id})

def contact(request):
    contacts = Contact.objects.all()
    return render(request, 'dashboard/contact.html', {'contacts': contacts})

def sendMessage(request):
    all_sms = SMSLog.objects.all()
    if request.method == 'POST':
        recipients = request.POST.get("recipients").split(",")
        recipients = [recipient.strip() for recipient in recipients]
        message = request.POST.get('message')
        response = send_sms(recipients, message)
        
        SMSLog.objects.create(
            recipients=", ".join(recipients),
            message=message, 
            status=response.get('status'), 
            response=response,
        )
        return JsonResponse(response)
    context = {
        'all_sms': all_sms
    }
    return render(request, 'dashboard/sendMessage.html', context)

def bookings(request):
    rentals = Rental.objects.all()
    return render(request, 'dashboard/bookings.html', {'rentals': rentals})

def appointments(request):
    all_appointments = Appointment.objects.all()
    return render(request, 'dashboard/appointments.html', {'all_appointments': all_appointments})
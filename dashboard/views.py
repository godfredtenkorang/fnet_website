from django.shortcuts import render, redirect, get_object_or_404
from rental.models import Contact, Rental, Appointment, Payment
from my_site.models import Car, Driver
from my_site.forms import DriverForm
from .utils import send_sms, appointment_update_sms, driver_license_sms
from .models import SMSLog
from django.http import HttpResponse

from expenses.models import Expense, MyCar, Receipt
from expenses.forms import ExpenseForm, ReceiptForm
from django.db.models import Sum
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import render_to_string

from django.db.models import Q
from rental.forms import AppointmentUpdateForm


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
        return redirect("sendMessage")
    context = {
        'all_sms': all_sms
    }
    return render(request, 'dashboard/sendMessage.html', context)

def bookings(request):
    rentals = Rental.objects.all()
    return render(request, 'dashboard/bookings.html', {'rentals': rentals})

def booking_payments(request):
    payments = Payment.objects.all()
    return render(request, 'dashboard/booking_payments.html', {'payments': payments})

def print_payment_receipt(request, receipt_id):
    payment = Payment.objects.get(id=receipt_id)
    
    template_path = 'dashboard/receipt_book_template.html'
    context = {'payment': payment}
    
    html = render_to_string(template_path, context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename"receipt_{payment.id}.pdf"'
    pisa_status = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=response, encoding='UTF-8')
    
    if pisa_status.err:
        return HttpResponse('Error generating PDF', content_type='text/plain')
    return response

def appointments(request):
    all_appointments = Appointment.objects.all()
    return render(request, 'dashboard/appointments.html', {'all_appointments': all_appointments})

def add_expenses(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_expenses')
    else:
        form = ExpenseForm()
    return render(request, 'dashboard/expenses/add_expense.html', {'form': form})

def view_expenses(request):
    car_id = request.GET.get('car', None)
    month = request.GET.get('month', None)
    expenses = Expense.objects.all()
    car_name = 'All Cars'
    month_name = 'All Months'
    if car_id:
        car = get_object_or_404(MyCar, id=car_id)
        expenses = expenses.filter(car_id=car_id)
        car_name = car.name
    if month:
        expenses = expenses.filter(month=month)
        month_name = month
        
    total_amount = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    totals = expenses.aggregate(
        total_amount_received=Sum('amount_received'),
        total_drivers_commission=Sum('drivers_commission'),
        total_other_expenses=Sum('other_expenses'),
        total_amount=Sum('amount')
    )
    
    all_totals = Expense.objects.aggregate(
        total_amount_received=Sum('amount_received'),
        total_drivers_commission=Sum('drivers_commission'),
        total_other_expenses=Sum('other_expenses'),
        total_amount=Sum('amount')
    )
    
    return render(request, 'dashboard/expenses/view_expenses.html', {
        'expenses': expenses,
        'cars': MyCar.objects.all(),
        'car': car_name,
        'month': month_name,
        'total_amount': total_amount,
        'totals': totals,
        'all_totals': all_totals,
    })
    
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=result)
    if pisa_status.err:
        return HttpResponse(f"We had some errors <pre>{html}</pre>")
    return result

def get_pdf(request):
      
    
    return render(request, 'dashboard/expenses/get_pdf.html', {
        
        'cars': MyCar.objects.all(),
        
        
    })
    
    
def download_pdf(request):
    car_id = request.GET.get('car', None)
    month = request.GET.get('month', None)
    expenses = Expense.objects.all()
    car_name = 'All Cars'
    month_name = 'All Months'
    if car_id:
        car = get_object_or_404(MyCar, id=car_id)
        expenses = expenses.filter(car_id=car_id)
        car_name = car.name
    if month:
        expenses = expenses.filter(month=month)
        month_name = month
        
    totals = expenses.aggregate(
        total_amount_received=Sum('amount_received'),
        total_drivers_commission=Sum('drivers_commission'),
        total_other_expenses=Sum('other_expenses'),
        total_amount=Sum('amount')
    )
    
    all_totals = Expense.objects.aggregate(
        total_amount_received=Sum('amount_received'),
        total_drivers_commission=Sum('drivers_commission'),
        total_other_expenses=Sum('other_expenses'),
        total_amount=Sum('amount')
    )
    
    context = {
        'expenses': expenses,
        'car': car_name,
        'month': month_name,
        'totals': totals,
        'all_totals': all_totals,
    }
    return render_to_pdf('dashboard/expenses/pdf_template.html', context)

    
def register_driver(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('driver-list')
    else:
        form = DriverForm()
    return render(request, 'dashboard/driver/driver_form.html', {'form': form})

def driver_list(request):
    drivers = Driver.objects.all()
    return render(request, 'dashboard/driver/driver_list.html', {'drivers': drivers})

def assign_driver(request, car_id):
    # Fetch the specific car by its ID
    car = get_object_or_404(Car, id=car_id)
    
    # Fetch all available drivers
    drivers = Driver.objects.filter(is_available=True)
    
    if request.method == 'POST':
        driver_id = request.POST.get('driver_id')
        driver = get_object_or_404(Driver, id=driver_id)
        car.driver = driver
        car.save()
        driver.is_available = False
        driver.save()
        return redirect('dashboard')
    context = {
        'car': car,
        'drivers': drivers,
    }
    return render(request, 'dashboard/driver/assign_driver.html', context)


def update_appointment(request, appointment_id):
    # Get the specific appointment by its ID
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        form = AppointmentUpdateForm(request.POST, instance=appointment)
        if form.is_valid():
            update_appointment = form.save()
            
            if update_appointment.driver:
                update_appointment.driver.is_available == False
                update_appointment.driver.save()
                
            appointment_update_sms(appointment.customer_phone, appointment.customer_name, appointment.appointment_date, appointment.appointment_time, appointment.driver)
            return redirect('appointments')  # Redirect to the appointment list or another relevant page
    else:
        form = AppointmentUpdateForm(instance=appointment)

    return render(request, 'dashboard/appointment_forms.html', {
        'appointment': appointment,
        'form': form,
    })
    
    
def complete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if appointment.status != 'Completed':
        commission = appointment.calculate_commission()
        
        if appointment.driver:
            appointment.driver.commission += commission
            appointment.driver.save()
            
        appointment.status = 'Completed'
        appointment.save()
        
    return redirect('appointments')



def driver_dashboard(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    appointments = Appointment.objects.filter(driver=driver, status='Completed')
    total_commission = driver.commission
    
    return render(request, 'dashboard/driver/driver_dashboard.html', {
        'driver': driver,
        'appointments': appointments,
        'total_commission': total_commission,
    })

# message = (
#                 f"Dear {driver.first_name}, your driver's license "
#                 f"(License Number: {driver.licence_number}) is expiring on {driver.licence_expiry_date}. "
#                 "Please renew it as soon as possible to avoid issues."
#             )


def create_receipt(request):
    if request.method == 'POST':
        form = ReceiptForm(request.POST)
        if form.is_valid():
            receipt = form.save()
            return redirect('print-receipt', receipt_id=receipt.id)
    else:
        form = ReceiptForm()
    return render(request, 'dashboard/create_receipt.html', {'form': form})


def print_receipt(request, receipt_id):
    receipt = Receipt.objects.get(id=receipt_id)
    
    template_path = 'dashboard/receipt_template.html'
    context = {'receipt': receipt}
    
    html = render_to_string(template_path, context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename"receipt_{receipt.id}.pdf"'
    pisa_status = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=response, encoding='UTF-8')
    
    if pisa_status.err:
        return HttpResponse('Error generating PDF', content_type='text/plain')
    return response
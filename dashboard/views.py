from django.shortcuts import render, redirect, get_object_or_404
from rental.models import Contact, Rental, Appointment, Payment, RentalPayment
from my_site.models import Car, Driver, DriverReview, Agent
from my_site.forms import DriverForm, CarUpdateForm, AddGalleryForm, AgentForm
from .utils import send_sms, appointment_update_sms, driver_license_sms, rental_update_sms, rental_payment_update_sms, driver_send_sms, driver_register_sms, send_customer_sms_for_images, rental_driver_update_sms
from .models import SMSLog, DriversSMSLog, LoadCarImagesForCustomer
from django.http import HttpResponse, JsonResponse

from expenses.models import Expense, Receipt, Service
from expenses.forms import ReceiptForm
from django.db.models import Sum
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import render_to_string

from django.db.models import Q
from rental.forms import AppointmentUpdateForm, RentalUpdateForm, RentalPaymentUpdateForm
from decimal import Decimal

from agreements.models import *
from agreements.forms import *
from .forms import LoadImageForCustomerForm

from flight.models import Booking
from flight.forms import UpdateFlightBooking
from flight.utils import update_flight_sms

from users.models import User, Profile

from my_site.utils import send_review_sms

from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from users.utils import send_payment_sms
from django.contrib.auth.decorators import login_required

from rent.models import PropertyBooking
from rent.utils import send_approve_sms

User = get_user_model()

def all_users(request):
    users = User.objects.all()
    context = {
        'users': users,
        'title': 'Users'
    }
    return render(request, "dashboard/all_users.html", context)

@staff_member_required
def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_blocked = not user.is_blocked # Toggle block status
    user.save()
    status = "blocked" if user.is_blocked else "unblocked"
    messages.success(request, f"User {user.username} has been {status}")
    return redirect("manage_users")


def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, f"User {user.username} has been deleted.")
    return redirect("manage_users")



def dashboard(request):
    cars_available = Car.objects.count()
    bookings_id = Rental.objects.count()
    schedules_id = Appointment.objects.count()
    customers_id = User.objects.filter(role='customer').count()
    driver_id = User.objects.filter(role='driver').count()
    agent_id = User.objects.filter(role='agent').count()
    context = {
        'cars_available': cars_available,
        'bookings_id': bookings_id + schedules_id,
        'customers_id': customers_id,
        'driver_id': driver_id,
        'agent_id': agent_id,
        'title':'Dashboard'
    }
    return render(request, 'dashboard/dashboard.html', context)

def all_cars(request):
    cars = Car.objects.all()
    context = {
        'cars': cars,
        'title': 'All Cars'
    }
    return render(request, 'dashboard/cars/all_cars.html', context)


def all_cars_form(request, car_slug):
    car = get_object_or_404(Car, slug=car_slug)
    if request.method == 'POST':
        form = CarUpdateForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('all-cars')
    else:
        form = CarUpdateForm(instance=car)
    context = {
        'form': form,
        'car': car,
        'title': 'Car Detail'
    }
    return render(request, 'dashboard/cars/all_cars_form.html', context)


def contact(request):
    contacts = Contact.objects.all()
    return render(request, 'dashboard/contact.html', {'title': 'Contact', 'contacts': contacts})

def sendMessage(request):
    all_sms = SMSLog.objects.all()
    if request.method == 'POST':
        recipients = list(User.objects.filter(role='customer').values_list('phone', flat=True).distinct())
        
        message = request.POST.get('message')
        response = send_sms(recipients, message)
        
        SMSLog.objects.create(
            recipients=recipients,
            message=message, 
            status=response.get('status'), 
            response=response,
        )
        return redirect("sendMessage")
        
    
    context = {
        'all_sms': all_sms,
        'title': 'SMS to Customers'
    }
    return render(request, 'dashboard/sendMessage.html', context)

def sendDriverMessage(request):
    all_driver_sms = DriversSMSLog.objects.all()
    if request.method == 'POST':
        phone_numbers = list(User.objects.filter(role='driver').values_list('phone', flat=True).distinct())
        
        messages = request.POST.get('messages')
        response = driver_send_sms(phone_numbers, messages)
        
        DriversSMSLog.objects.create(
            recipients=phone_numbers,
            message=messages, 
            status=response.get('status'), 
            response=response,
        )
        return redirect("sendDriverMessage")
    
    context = {
        'all_driver_sms': all_driver_sms,
        'title': 'SMS to Driver'
    }
    return render(request, 'dashboard/sms_message_to_drivers.html', context)


def bookings(request):
    rentals = Rental.objects.all()
    return render(request, 'dashboard/bookings.html', {'title': 'Bookings', 'rentals': rentals})

def update_rentals(request, rental_id):
    # Get the specific appointment by its ID
    rental = get_object_or_404(Rental, id=rental_id)
    
    if request.method == 'POST':
        form = RentalUpdateForm(request.POST, instance=rental)
        if form.is_valid():
            update_rentals = form.save()
            
            if update_rentals.driver:
                update_rentals.driver.is_available == False
                update_rentals.driver.save()
                
            # vat_percentage = Decimal(0.25) # 25% VAT

            # form.vat_amount = form.total_price * vat_percentage

            # form.base_price = form.total_price - form.vat_amount
            
            # form.total_price = form.base_price + form.vat_amount
            
                
            rental_update_sms(rental.customer_phone, rental.customer_name, rental.status, rental.pick_up_time, rental.drop_off_time, rental.rental_date, rental.rental_date, rental.location_category, rental.town, rental.driver, rental.total_price, rental.id)
            rental_driver_update_sms(rental.driver.phone_number, rental.driver.first_name, rental.rental_date, rental.pick_up_time, rental.drop_off_time, rental.town, rental.city, rental.customer_name, rental.customer_phone)
            return redirect('bookings')  # Redirect to the rentals list or another relevant page
    else:
        form = RentalUpdateForm(instance=rental)

    return render(request, 'dashboard/booking_forms_update.html', {
        'rental': rental,
        'form': form,
        'title': 'Bookings',
    })
    
def complete_rental(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)
    
    if rental.status != 'Completed':
        
        commission = rental.calculate_commission()
        commission = rental.calculate_agent_commission()
        
        
        if rental.driver and rental.agent:
            rental.driver.commission += commission
            rental.agent.commission += commission
            rental.driver.is_available = True
            rental.driver.save()
            rental.agent.save()
            
        rental.status = 'Completed'
        rental.save()
        
        customer = rental.customer
        driver = rental.driver
        review_link = f"https://tlghana.com/review/{driver.id}/"
        
        message = {
            f"Dear {customer.username}, your trip with {driver.first_name} has been completed. "
            f"We would love to hear your feedback. Please rate your driver: {review_link}"
        }
        
        send_review_sms(customer.phone, message)
        
    return redirect('bookings')


def all_reviews(request):
    reviews = DriverReview.objects.all()
    context = {
        'reviews': reviews,
        'title': 'Reviews'
    }

    return render(request, 'dashboard/all_reviews.html', context)

def print_rental_receipt(request, receipt_id):
    rental = Rental.objects.get(id=receipt_id)
    
    template = get_template('dashboard/receipt_rental_template.html')
    html = template.render({'rental': rental})
    result = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=result)
    if pisa_status.err:
        return HttpResponse(f"We had some errors <pre>{html}</pre>")
    return result


def booking_payments(request):
    payments = Payment.objects.all()
    return render(request, 'dashboard/booking_payments.html', {'title': 'Bookings', 'payments': payments})

def update_rental_payment(request, rental_id):
    # Get the specific appointment by its ID
    rental_payment = get_object_or_404(Payment, id=rental_id)
    
    if request.method == 'POST':
        form = RentalPaymentUpdateForm(request.POST, instance=rental_payment)
        if form.is_valid():
            update_rental_payment = form.save()
            
            if update_rental_payment.driver:
                update_rental_payment.driver.is_available == False
                update_rental_payment.driver.save()
                
            rental_payment_update_sms(rental_payment.customer_phone, rental_payment.customer_name, rental_payment.rental_date, rental_payment.rental_date, rental_payment.driver)
            return redirect('booking_payments')  # Redirect to the rentals list or another relevant page
    else:
        form = RentalPaymentUpdateForm(instance=rental_payment)

    return render(request, 'dashboard/booking_payment_form.html', {
        'rental_rental': rental_payment,
        'form': form,
        'title': 'Update Bookings',
    })
    
def complete_rental_payment(request, rental_id):
    rental_payment = get_object_or_404(Payment, id=rental_id)
    
    if rental_payment.status != 'Completed':
        commission = rental_payment.commission_rate
        
        
        if rental_payment.driver:
            rental_payment.driver.commission += commission
            rental_payment.driver.save()
            
        rental_payment.status = 'Completed'
        rental_payment.save()
        
    return redirect('booking_payments')
    


def print_payment_receipt(request, receipt_id):
    payment = Payment.objects.get(id=receipt_id)
    
    template = get_template('dashboard/receipt_book_template.html')
    html = template.render({'payment': payment})
    result = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=result)
    if pisa_status.err:
        return HttpResponse(f"We had some errors <pre>{html}</pre>")
    return result
    


def appointments(request):
    all_appointments = Appointment.objects.all()
    return render(request, 'dashboard/appointments.html', {'title': 'All Schedules', 'all_appointments': all_appointments})

def add_expenses(request):
    cars = Car.objects.all()
    if request.method == 'POST':
        car_id = request.POST.get('car')
        date = request.POST.get('date')
        amount_received = request.POST.get('amount_received')
        other_expenses = request.POST.get('other_expenses')
        description = request.POST.get('description')
        month = request.POST.get('month')
        
        car = get_object_or_404(Car, id=car_id)
        
        get_amount_receiced = Decimal(amount_received)
        get_other_expenses = Decimal(other_expenses)
        
        total_amount = get_amount_receiced - get_other_expenses
        
        get_total_amount = Decimal(total_amount)
        
        expenses = Expense(car=car, amount_received=amount_received, date=date, description=description, other_expenses=other_expenses, amount=get_total_amount, month=month)
        expenses.save()
        return redirect('view_expenses')
        
    # if request.method == 'POST':
    #     form = ExpenseForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('view_expenses')
    # else:
    #     form = ExpenseForm()
    return render(request, 'dashboard/expenses/add_expense.html', {'cars': cars, 'title': 'Add Expense'})

def view_expenses(request):
    car_id = request.GET.get('car', None)
    month = request.GET.get('month', None)
    expenses = Expense.objects.all()
    car_name = 'All Cars'
    month_name = 'All Months'
    if car_id:
        car = get_object_or_404(Car, id=car_id)
        expenses = expenses.filter(car_id=car_id)
        car_name = car.car_name
    if month:
        expenses = expenses.filter(month=month)
        month_name = month
        
    total_amount = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    totals = expenses.aggregate(
        total_amount_received=Sum('amount_received'),
        total_other_expenses=Sum('other_expenses'),
        total_amount=Sum('amount')
    )
    
    all_totals = Expense.objects.aggregate(
        total_amount_received=Sum('amount_received'),
        total_other_expenses=Sum('other_expenses'),
        total_amount=Sum('amount')
    )
    
    return render(request, 'dashboard/expenses/view_expenses.html', {
        'expenses': expenses,
        'cars': Car.objects.all(),
        'car': car_name,
        'month': month_name,
        'total_amount': total_amount,
        'totals': totals,
        'all_totals': all_totals,
        'title': 'View Expenses',
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
        
        'cars': Car.objects.all(),
        
        
    })
    
    
def download_pdf(request):
    car_id = request.GET.get('car', None)
    month = request.GET.get('month', None)
    expenses = Expense.objects.all()
    car_name = 'All Cars'
    month_name = 'All Months'
    if car_id:
        car = get_object_or_404(Car, id=car_id)
        expenses = expenses.filter(car_id=car_id)
        car_name = car.car_name
    if month:
        expenses = expenses.filter(month=month)
        month_name = month
        
    totals = expenses.aggregate(
        total_amount_received=Sum('amount_received'),
        total_other_expenses=Sum('other_expenses'),
        total_amount=Sum('amount')
    )
    
    all_totals = Expense.objects.aggregate(
        total_amount_received=Sum('amount_received'),
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


def services(request):
    return render(request, 'dashboard/all_services.html')

def register_agent(request):
    if request.method == 'POST':
        form = AgentForm(request.POST)
        if form.is_valid():
            forms = form.save()
            return redirect('agent-list')
    else:
        form = AgentForm()
    context = {
        'title': 'Register Agent',
        'form': form,
    }
    return render(request, 'dashboard/agent/register.html', context)

def agent_list(request):
    agents = Agent.objects.all()
    context = {
        'agents': agents,
        'title': 'Agent Lists',
    }
    return render(request, 'dashboard/agent/agent_lists.html', context)

def agent_detail(request, agent_id):
    agent = get_object_or_404(Agent, id=agent_id)
    context = {
        'agent': agent,
        'title': 'Agent Detail'
    }
    return render(request, 'dashboard/agent/agent_detail.html', context)
    
def register_driver(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            forms = form.save()
            driver_register_sms(forms.phone_number, forms.first_name)
            return redirect('driver-list')
    else:
        form = DriverForm()
    return render(request, 'dashboard/driver/driver_form.html', {'title': 'Register Driver', 'form': form})

def driver_list(request):
    drivers = Driver.objects.all()
    return render(request, 'dashboard/driver/driver_list.html', {'title': 'All Drivers', 'drivers': drivers})

def driver_detail(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    if request.method == 'POST':
        driver_license_sms(driver.phone_number, driver.first_name, driver.licence_number, driver.licence_expiry_date)
    return render(request, 'dashboard/driver/driver_detail.html', {'title': 'Driver Detail', 'driver': driver})

def agent_dashboard(request, agent_id):
    agent = get_object_or_404(Agent, id=agent_id)
    appointments = Appointment.objects.filter(agent=agent, status='Completed')
    rentals = Rental.objects.filter(agent=agent, status='Completed')
    payments = Payment.objects.filter(agent=agent, status='Completed')
    total_commission = agent.commission
    
    return render(request, 'dashboard/agent/agent_dashboard.html', {
        'agent': agent,
        'appointments': appointments,
        'rentals': rentals,
        'payments': payments,
        'total_commission': total_commission,
        'title': 'Agent Dashboard',
    })

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
                
                
                
            appointment_update_sms(appointment.customer_phone, appointment.customer_name, appointment.status, appointment.schedule_date, appointment.pick_up_time, appointment.driver)
            return redirect('appointments')  # Redirect to the appointment list or another relevant page
    else:
        form = AppointmentUpdateForm(instance=appointment)

    return render(request, 'dashboard/appointment_forms.html', {
        'appointment': appointment,
        'form': form,
        'title': 'Update Schedule',
    })
    
    
def complete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if appointment.status != 'Completed':
        commission = appointment.commission_rate
        
        if appointment.driver:
            appointment.driver.commission += commission
            appointment.driver.save()
            
        appointment.status = 'Completed'
        appointment.save()
    
        
        customer = appointment.customer
        driver = appointment.driver
        review_link = f"https://tlghana.com/review/{driver.id}/"
        
        message = {
            f"Dear {customer.username}, your trip with {driver.first_name} has been completed. "
            f"We would love to hear your feedback. Please rate your driver: {review_link}"
        }
        
        send_review_sms(customer.phone, message)
        
    return redirect('appointments')



def driver_dashboard(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    appointments = Appointment.objects.filter(driver=driver, status='Completed')
    rentals = Rental.objects.filter(driver=driver, status='Completed')
    payments = Payment.objects.filter(driver=driver, status='Completed')
    total_commission = driver.commission
    
    return render(request, 'dashboard/driver/driver_dashboard.html', {
        'driver': driver,
        'appointments': appointments,
        'rentals': rentals,
        'payments': payments,
        'total_commission': total_commission,
        'title': 'Driver Dashboard',
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


def newReceipt(request):
    return render(request, 'dashboard/newReceipt.html')


def customer_lists(request):
    customers_info = User.objects.filter(role="customer").values("username", "phone")
    return render(request, 'dashboard/customer_list.html', {'title': 'All Customers', 'customers': customers_info})




def agreementForm(request):
   
    return render(request, 'dashboard/agreements/agreementForm.html')


def pay_and_move_form(request):
    if request.method == 'POST':
        form = PayAndMoveAgreementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pay_and_move_lists')
    else:
        form = PayAndMoveAgreementForm()
    return render(request, 'dashboard/agreements/pay_and_drive_form.html', {'form': form})

def pay_and_move_lists(request):
    lists = PayAndDriveAgreement.objects.all()
    return render(request, 'dashboard/agreements/pay_and_move_lists.html', {'lists': lists})

def driveAndPay(request, pdf):
    forms = PayAndDriveAgreement.objects.get(pk=pdf)
    
    template = get_template('dashboard/agreements/driveAndPay.html')
    html = template.render({'forms': forms})
    result = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=result)
    if pisa_status.err:
        return HttpResponse(f"We had some errors <pre>{html}</pre>")
    return result




def driver_agreement_form(request):
    if request.method == 'POST':
        form = DriverAgreementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('driver_agreement_lists')
    else:
        form = DriverAgreementForm()
    return render(request, 'dashboard/agreements/driver_agreement.html', {'form': form})


def driver_agreement_lists(request):
    lists = DriverAgreement.objects.all()
    return render(request, 'dashboard/agreements/driver_agreement_lists.html', {'lists': lists})

def driverAgreement(request, pdf):
    forms = DriverAgreement.objects.get(pk=pdf)
    
    template = get_template('dashboard/agreements/driverAgreement.html')
    html = template.render({'forms': forms})
    result = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=result)
    if pisa_status.err:
        return HttpResponse(f"We had some errors <pre>{html}</pre>")
    return result


def new_contract_list(request):
    lists = BoggasForm.objects.all()
    context = {
        'lists': lists,
        'title': 'Boggas Drive Form'
    }
    return render(request, 'dashboard/agreements/new_contract_list.html', context)

def new_contract_form(request):
    if request.method == 'POST':
        form = BoggasAgreementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('driver_agreement_lists')
    else:
        form = BoggasAgreementForm()
        
    context = {
        'form': form
    }
    return render(request, 'dashboard/agreements/new_contract.html', context)

def newContract(request, pdf):
    forms = DriverAgreement.objects.get(pk=pdf)
    
    template = get_template('dashboard/agreements/newConrtact.html')
    html = template.render({'forms': forms})
    result = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=result)
    if pisa_status.err:
        return HttpResponse(f"We had some errors <pre>{html}</pre>")
    return result
    



def add_gallery(request):
    if request.method == 'POST':
        form = AddGalleryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add-gallery')
    else:
        form = AddGalleryForm()
        
    context = {
        'form': form,
        'title': 'Gallery'
    }
    return render(request, 'dashboard/add_gallery.html', context)



def add_car_for_customer(request):
    if request.method == 'POST':
        form = LoadImageForCustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customers-with-images-lists')
        
    else:
        form = LoadImageForCustomerForm()
    
    context = {
        'form': form
    }
    return render(request, 'dashboard/car_image/add_car_for_customer.html', context)


def get_customers_with_images_upload(request):
    customer_id = request.GET.get('id', None)
    customers = User.objects.filter(role='customer')
    if customer_id:
        customer = get_object_or_404(User, id=customer_id)
        
        send_customer_sms_for_images(customer.phone, customer.username, customer.id)
        return JsonResponse({"message": "SMS sent successfully!"})  # AJAX response

    
    context = {
        'customers': customers
    }
    return render(request, 'dashboard/car_image/customers_with_images_list.html', context)


def get_customer_load_images(request, customer_id):
    customer = None
    get_images = LoadCarImagesForCustomer.objects.all()
    if customer_id:
        customer = get_object_or_404(User, id=customer_id)
        get_images = get_images.filter(customer=customer)
    context = {
        'customer': customer,
        'get_images': get_images
    }
    return render(request, 'dashboard/car_image/get_images.html', context)

def send_sms_to_customer(request):
    return render(request, 'dashboard/car_image/send_sms.html')



def flight_booking(request):
    bookings = Booking.objects.all()
    context = {
        'bookings': bookings
    }
    return render(request, 'dashboard/flight_booking.html', context)

def update_flight_booking(request, airline_id):
    airline = get_object_or_404(Booking, id=airline_id)
    if request.method == 'POST':
        form = UpdateFlightBooking(request.POST, instance=airline)
        if form.is_valid():
            forms = form.save()
            update_flight_sms(forms.phone_number, forms.full_name, forms.status, forms.airline, forms.category, forms.trip_from, forms.trip_to, forms.trip_departure, forms.trip_return, forms.number_of_adults, forms.number_of_children, forms.number_of_infants)
        return redirect('flight-booking')
    else:
        form = UpdateFlightBooking(instance=airline)
    context = {
        'airline': airline,
        'form': form,
    }
    return render(request, 'dashboard/update_flight_booking.html', context)

def all_profiles(request):
    profiles = Profile.objects.all()
    context = {
        'profiles': profiles,
        'title': 'Profiles'
    }
    return render(request, 'dashboard/all_profiles.html', context)

def all_payments(request):
    all_payments = RentalPayment.objects.all()
    context = {
        'all_payments': all_payments,
        'title': 'Payments'
    }
    return render(request, 'dashboard/all_payments.html', context)

def complete_rental_payment(request, payment_id):
    payment = get_object_or_404(RentalPayment, id=payment_id)
    
    if payment.is_approved != True:
        
        payment.is_approved = True
        payment.save()
        
        send_payment_sms(payment.rental.customer_phone, payment.rental.customer_name, payment.rental.total_price)
        
    return redirect('all_payments')


def property_bookings(request):
    properties = PropertyBooking.objects.all()
    context = {
        'properties': properties,
        'title': 'Properties Bookings'
    }
    return render(request, 'dashboard/property/bookings.html', context)

def approve_property(request, property_id):
    property = get_object_or_404(PropertyBooking, id=property_id)
    
    if property.is_approved != True:
        
        property.is_approved = True
        property.save()
        
        send_approve_sms(property.phone, property.name, property.property)
        
    return redirect('properties_bookings')
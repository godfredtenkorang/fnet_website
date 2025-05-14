from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.models import auth

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegisterForm, LoginForm, UserUpdateForm, ProfileUpdateForm
from .models import User, OTP
from rental.models import Rental, Appointment, RentalPayment
from .utils import generate_otp, send_otp_sms, send_otp, send_otp_whatsapp_mnotify
from django.contrib import messages
from my_site.models import Driver, Car, Agent
from flight.models import Booking
from users.models import User
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from rent.models import PropertyBooking
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.db.models import Sum, Max
from dashboard.forms import MileageRecordForm, FuelRecordForm, ExpenseForm, UpdateMileageRecordForm, OilChangeForm
from dashboard.models import MileageRecord, FuelRecord, Expense, OilChange
from django.utils import timezone


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False # Deactivate account until OTP is verified
            user.save()
            
            # Generate OTP and store it in session
            otp = generate_otp()
            request.session['registration_otp'] = otp
            request.session['registration_user_id'] = user.id
            
            send_otp_sms(user.phone, otp, user.username, form.cleaned_data['password1'])
            # if send_otp_whatsapp_mnotify(user.phone, otp, user.username, form.cleaned_data['password1']):
            #     messages.success(request, 'OTP sent to your WhatsApp.')
            return redirect("verify_registration_otp")
            # else:
            #     messages.error(request, 'Failed to sent OTP')
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


def verify_registration_otp(request):
    if request.method == 'POST':
        input_otp = request.POST.get('otp')
        session_otp = request.session.get('registration_otp')
        user_id = request.session.get('registration_user_id')
        
        if input_otp and session_otp and input_otp == session_otp:
            # OTP is correct. Activate the user and log them in.
            user = get_object_or_404(User, id=user_id)
            user.is_active = True
            user.save()
            backend = 'users.backends.EmailOrUsernameBackend'  # Replace if needed
        
            user.backend = backend
        
            login(request, user)
            
            # Clean up session data
            del request.session['registration_otp']
            del request.session['registration_user_id']
            
            messages.success(request, "Registration complete! You are now logged in.")
            return redirect("index")
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'users/verify_registration_otp.html')

def login_user(request):

    if request.method == 'POST':
        
        username_or_phone = request.POST.get('username_or_phone')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username_or_phone, password=password)
        
        backend = 'users.backends.EmailOrUsernameBackend'  # Replace if needed
        
        user.backend = backend
        
        try:
            if user:
                login(request, user)
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            else:
                return render(request, "users/login.html", {"error": "Invalid credentials"})
            
        except:
            if user is not None:
                if user.role == "admin":
                    return redirect("dashboard")
                elif user.role == "customer":
                    return redirect("customer_dashboard")
                elif user.role == "driver":
                    return redirect("driver_dashboard")
                else:
                    return redirect("agent_dashboard")
            else:
                return render(request, "users/login.html", {"error": "Invalid credentials"})

    context = {
        'title': 'Login'
    }
    
    return render(request, 'users/login.html', context)


def request_reset_otp(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        user = User.objects.filter(phone=phone_number).filter()
        if user:
            send_otp(phone_number)
            return redirect('verify_otp_and_reset_password')
    return render(request, 'users/request_otp.html')
    


def verify_otp_and_reset_password(request):
    if request.method == 'POST':
        phone_number = request.POST.get("phone_number")
        otp_code = request.POST.get("otp_code")
        new_password = request.POST.get("new_password")
        
        otp = OTP.objects.filter(phone=phone_number, otp_code=otp_code).first()
        
        if otp and otp.is_valid():
            user = get_object_or_404(User, phone=phone_number)
            user.password = make_password(new_password)
            user.save()
            otp.delete() # Remove OTP after successful use
            return redirect('login')
    return render(request, 'users/reset_password.html')


def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    
    return render(request, 'users/profile.html', context)

def logout(request):
    auth.logout(request)
    
    return redirect('login')



@csrf_exempt
def mnotify_callback(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))

            # Example: Log or process the response data
            print("MNotify Callback Data:", data)

            # You could save this info to your database if needed
            # For example: message_id, status, recipient, etc.

            return JsonResponse({"message": "Callback received successfully"}, status=200)

        except Exception as e:
            print("Error processing callback:", e)
            return JsonResponse({"error": "Invalid data"}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)



# Role-based access control
def is_customer(user):
    return user.role == "customer"

def is_driver(user):
    return user.role == "driver"

def is_agent(user):
    return user.role == "agent"


# ------------------ Customer Dashboard Start--------------------------
@login_required
@user_passes_test(is_customer)
def customer_dashboard(request):
    cars_available = Car.objects.count()
    bookings_id = Rental.objects.filter(customer=request.user, status='Completed').count()
    schedules_id = Appointment.objects.filter(customer=request.user, status='Completed').count()
    context = {
        'cars_available': cars_available,
        'bookings_id': bookings_id,
        'schedules_id': schedules_id
    }
    return render(request, "users/customer_dashboard/dashboard.html", context)

def customer_bookings(request):
    bookings = Rental.objects.filter(customer=request.user)
    context = {
        'bookings': bookings,
        'title': 'Customer Bookings'
    }
    
    return render(request, "users/customer_dashboard/booking.html", context)

def customer_schedules(request):
    bookings = Appointment.objects.filter(customer=request.user)
    context = {
        'bookings': bookings,
        'title': 'Customer Schedules'
    }
    
    return render(request, "users/customer_dashboard/schedule.html", context)

def customer_flight_booking(request):
    bookings = Booking.objects.filter(customer=request.user)
    context = {
        'bookings': bookings,
        'title': 'Customer Flights'
    }
    
    return render(request, "users/customer_dashboard/flight_booking.html", context)

@login_required
def payment(request):
    bookings = Rental.objects.filter(customer=request.user)
    context = {
        'bookings': bookings,
        'title': 'Customer Bookings'
    }
    return render(request, "users/customer_dashboard/payment.html", context)

@login_required
def payment_detail(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        payment_code = request.POST.get('payment_code')
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        transaction_id = request.POST.get('transaction_id')
        
        payments = RentalPayment(rental=rental, payment_method=payment_method, payment_code=payment_code, name=name, amount=amount, transaction_id=transaction_id)
        payments.save()
        
        return redirect('customer-payment')

    context = {
        'rental': rental,
        'title': 'Customer Bookings'
    }
    return render(request, "users/customer_dashboard/payment_form.html", context)

@login_required
def all_properies_bookings(request):
    properties = PropertyBooking.objects.filter(user=request.user)
    context = {
        'properties': properties,
        'title': 'Customer Properties'
    }
    return render(request, "users/customer_dashboard/properties.html", context)


# ------------------ Customer Dashboard End--------------------------


# ------------------ Driver Dashboard Start--------------------------

@login_required
@user_passes_test(is_driver)
def driver_dashboard(request):
    cars_available = Car.objects.count()
    driver = get_object_or_404(Driver, driver=request.user)
    bookings_id = Rental.objects.filter(driver=driver, status='Completed').count()
    schedules_id = Appointment.objects.filter(driver=driver, status='Completed').count()
    context = {
        'cars_available': cars_available,
        'bookings_id': bookings_id + schedules_id,
    }
    return render(request, "users/driver_dashboard/dashboard.html", context)

def driver_detail(request):
    drivers = Driver.objects.filter(driver=request.user)
    context = {
        'drivers': drivers
    }
    return render(request, "users/driver_dashboard/my_detail.html", context)

def driver_trips(request):
    driver = get_object_or_404(Driver, driver=request.user)
    rentals = Rental.objects.filter(driver=driver)
    context = {
        'rentals': rentals,
        'title': 'Driver Bookings'
    }
    
    return render(request, "users/driver_dashboard/trips.html", context)

def driver_book(request):
    driver = get_object_or_404(Driver, driver=request.user)
    rentals = Rental.objects.filter(driver=driver, status='Completed')
    schedules = Appointment.objects.filter(driver=driver, status='Completed')
    context = {
        'driver': driver,
        'rentals': rentals,
        'schedules': schedules,
        'total_commission': driver.commission
    }
    return render(request, "users/driver_dashboard/driver_book.html", context)


def add_mileage(request):
    driver = request.user
    if request.method == 'POST':
        form = MileageRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.driver = driver
            record.save()
            return redirect('driver_dashboard')
    else:
        form = MileageRecordForm()
        
    context = {
        'form': form,
        'title': 'Add Mileage'
    }
    return render(request, 'users/driver_dashboard/add_mileage.html', context)

def view_mileage(request):
    driver = request.user
    records = MileageRecord.objects.filter(driver=driver).order_by('-date')
    
    
        
    context = {
        'driver': driver,
        'records': records,
        'title': 'View Mileage'
    }
    return render(request, 'users/driver_dashboard/detail/view_mileage.html', context)


def update_mileage(request, mileage_id):
    
    mileage = get_object_or_404(MileageRecord, id=mileage_id)
    
    if request.method == 'POST':
        form = UpdateMileageRecordForm(request.POST, instance=mileage)
        if form.is_valid():
            update_mileage = form.save(commit=False)
            update_mileage.save()
            messages.success(request, 'Mileage Updated Successfully!')
            return redirect('view-mileage')
        
    else:
        form = UpdateMileageRecordForm(instance=mileage)
    
    context = {
        'mileage': mileage,
        'form': form,
        'title': 'Update Mileage'
    }
    
    return render(request, 'users/driver_dashboard/detail/update_mileage.html', context)

def mileage(request):
    driver = request.user
    vehicles = Car.objects.filter(
        mileagerecord__driver=driver
    ).distinct().annotate(
        latest_mileage=Max('mileagerecord__end_mileage')
    )
    
    for vehicle in vehicles:
        # Calculate remaining mileage safely
        if vehicle.last_oil_change_mileage is None:
            vehicle.remaining_mileage = vehicle.oil_change_default
        else:
            vehicle.remaining_mileage = max(
                (vehicle.last_oil_change_mileage + vehicle.oil_change_default) - 
                (vehicle.latest_mileage or 0),
                0
            )
    context = {
        'vehicles': vehicles,
        'title': 'Vehicles'
    }
    return render(request, 'users/driver_dashboard/mileage.html', context)


def vehicle_maintenance(request, vehicle_id):
    vehicle = get_object_or_404(Car, id=vehicle_id)
    
    oil_changes = OilChange.objects.filter(vehicle=vehicle).order_by('-date')
    
    latest_mileage = vehicle.mileagerecord_set.order_by('-date').first()
    
    context = {
        'vehicle': vehicle,
        'oil_changes': oil_changes,
        'latest_mileage': latest_mileage,
        'needs_oil_change': vehicle.needs_oil_change
    }
    
    return render(request, 'users/driver_dashboard/maintenance/vehicle_maintenance.html', context)

def record_oil_change(request, vehicle_id):
    driver = request.user
    vehicle = get_object_or_404(Car, id=vehicle_id)
    
    if request.method == 'POST':
        form = OilChangeForm(request.POST)
        if form.is_valid():
            oil_change = form.save(commit=False)
            oil_change.driver = driver
            oil_change.vehicle = vehicle
            oil_change.save()
            # Reset the oil change tracking
            vehicle.reset_oil_change_tracking(oil_change.mileage)
            # Reset the oil change tracking
            vehicle.reset_oil_change_tracking(oil_change.mileage)
            return redirect('vehicle_maintenance', vehicle_id=vehicle.id)
    else:
        latest_mileage = vehicle.mileagerecord_set.order_by('-date').first()
        
        initial = {
            'mileage': latest_mileage.end_mileage if latest_mileage else 0,
            'date': timezone.now().date(),
        }
        
        form = OilChangeForm(initial=initial)
        
    context = {
        'form': form,
        'vehicle': vehicle,
    }
    
    return render(request, 'users/driver_dashboard/maintenance/record_oil_change.html', context)

def add_fuel(request):
    
    driver = request.user
    if request.method == 'POST':
        form = FuelRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.driver = driver
            record.save()
            return redirect('driver_dashboard')
    else:
        form = FuelRecordForm()
        
    context = {
        'form': form,
        'title': 'Add Fuel'
    }
    return render(request, 'users/driver_dashboard/add_fuel.html', context)

def view_fuel(request):
    driver = request.user
    records = FuelRecord.objects.filter(driver=driver).order_by('-date')
    
    
        
    context = {
        'driver': driver,
        'records': records,
        'title': 'View Fuel'
    }
    return render(request, 'users/driver_dashboard/detail/view_fuel.html', context)

def add_expenses(request):
    driver = request.user
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.driver = driver
            expense.save()
            return redirect('driver_dashboard')
    else:
        form = ExpenseForm()
        
    context = {
        'form': form,
        'title': 'Add Expense'
    }
    return render(request, 'users/driver_dashboard/add_expense.html', context)

def view_expenses(request):
    driver = request.user
    records = Expense.objects.filter(driver=driver).order_by('-date')
    
    
        
    context = {
        'driver': driver,
        'records': records,
        'title': 'View Expenses'
    }
    return render(request, 'users/driver_dashboard/detail/view_expense.html', context)

# ------------------ Driver Dashboard End--------------------------

@login_required
@user_passes_test(is_agent)
def agent_dashboard(request):
    return render(request, "users/agent_dashboard/dashboard.html")


def agent_trips(request):
    agent = get_object_or_404(Agent, agent=request.user)
    rentals = Rental.objects.filter(agent=agent)
    context = {
        'rentals': rentals,
        'title': 'Agent Bookings'
    }
    
    return render(request, "users/agent_dashboard/trips.html", context)

def agent_detail(request):
    agents = Agent.objects.filter(agent=request.user)
    context = {
        'agents': agents
    }
    return render(request, "users/agent_dashboard/my_detail.html", context)

def agent_book(request):
    agent = get_object_or_404(Agent, agent=request.user)
    rentals = Rental.objects.filter(agent=agent, status='Completed')
    schedules = Appointment.objects.filter(agent=agent, status='Completed')
    context = {
        'agent': agent,
        'rentals': rentals,
        'schedules': schedules,
        'total_commission': agent.commission
    }
    return render(request, "users/agent_dashboard/agent_book.html", context)

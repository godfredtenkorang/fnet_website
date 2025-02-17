from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.models import auth

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegisterForm, LoginForm, UserUpdateForm, ProfileUpdateForm
from .models import User, OTP
from rental.models import Rental, Appointment, RentalPayment
from .utils import generate_otp, send_otp_sms, send_otp
from django.contrib import messages
from my_site.models import Driver, Car, Agent
from flight.models import Booking
from users.models import User
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from rent.models import PropertyBooking


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
            
            send_otp_sms(user.phone, otp)
            
            
            return redirect("verify_registration_otp")
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
            login(request, user)
            
            # Clean up session data
            del request.session['registration_otp']
            del request.session['registration_user_id']
            
            messages.success(request, "Registration complete! You are now logged in.")
            return redirect("login")
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'users/verify_registration_otp.html')

def login_user(request):
    form = LoginForm()
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            try:
                if user:
                    login(request, user)
                    next_url = request.GET.get('next', '/')
                    return redirect(next_url)
                
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
        form = LoginForm()
        
    context = {
        'form': form,
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
        transaction_id = request.POST.get('transaction_id')
        
        payments = RentalPayment(rental=rental, payment_method=payment_method, payment_code=payment_code, transaction_id=transaction_id)
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

from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.models import auth

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegisterForm, LoginForm
from .models import User
from rental.models import Rental, Appointment
from .utils import generate_otp, send_otp_sms
from django.contrib import messages
from my_site.models import Driver, Car
from users.models import User


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
            
            if user is not None:
                login(request, user)
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
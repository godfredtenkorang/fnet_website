from django.shortcuts import render, redirect

from django.contrib.auth.models import auth

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegisterForm, LoginForm
from .models import User

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


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
                if user.role == "customer":
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



@login_required
@user_passes_test(is_customer)
def customer_dashboard(request):
    return render(request, "users/customer_dashboard/dashboard.html")

@login_required
@user_passes_test(is_driver)
def driver_dashboard(request):
    return render(request, "users/driver_dashboard/dashboard.html")

@login_required
@user_passes_test(is_agent)
def agent_dashboard(request):
    return render(request, "users/agent_dashboard/dashboard.html")
from django.shortcuts import render, redirect

from django.contrib.auth.models import auth

from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm



def login(request):
    form = LoginForm()
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth.login(request, user)
                
                return redirect("dashboard")
        
    context = {
        'form': form,
        'title': 'Login'
    }
    
    return render(request, 'users/login.html', context)


def logout(request):
    auth.logout(request)
    
    return redirect('login')
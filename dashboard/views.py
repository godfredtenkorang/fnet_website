from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def contact(request):
    return render(request, 'dashboard/contact.html')

def sendMessage(request):
    return render(request, 'dashboard/sendMessage.html')

def bookings(request):
    return render(request, 'dashboard/bookings.html')

from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'my_site/index.html')

def carDetail(request):
    return render(request, 'my_site/carDetail.html')

def rentCars(request):
    return render(request, 'my_site/rentCars.html')

def aboutUs(request):
    return render(request, 'my_site/aboutUs.html')

def service(request):
    return render(request, 'my_site/service.html')

def contactUs(request):
    return render(request, 'my_site/contactUs.html')

def booking(request):
    return render(request, 'my_site/booking.html')
def bookings(request):
    return render(request, 'my_site/bookings.html')

def signUp(request):
    return render(request, 'my_site/signUp.html')

def login(request):
    return render(request, 'my_site/login.html')

def termsAndCondition(request):
    return render(request, 'my_site/termsAndCondition.html')

def home(request):
    return render(request, 'my_site/home.html')

def sendMessage(request):
    return render(request, 'my_site/sendMessage.html')


def contact(request):
    return render(request, 'my_site/contact.html')

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
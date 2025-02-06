from django.shortcuts import render

# Create your views here.
def rent_house(request):
    return render(request, 'rent/rent_house.html')
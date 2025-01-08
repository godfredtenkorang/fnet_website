from django.shortcuts import render, redirect, get_object_or_404
from rental.models import Contact, Rental, Appointment
from my_site.models import Car
from .utils import send_sms
from .models import SMSLog
from django.http import HttpResponse

from expenses.models import Expense, MyCar
from expenses.forms import ExpenseForm
from django.db.models import Sum
from django.template.loader import get_template
from xhtml2pdf import pisa


# Create your views here.
def dashboard(request):
    cars_available = Car.objects.count()
    bookings_id = Rental.objects.count()
    return render(request, 'dashboard/dashboard.html', {'cars_available': cars_available, 'bookings_id':bookings_id})

def contact(request):
    contacts = Contact.objects.all()
    return render(request, 'dashboard/contact.html', {'contacts': contacts})

def sendMessage(request):
    all_sms = SMSLog.objects.all()
    if request.method == 'POST':
        recipients = request.POST.get("recipients").split(",")
        recipients = [recipient.strip() for recipient in recipients]
        message = request.POST.get('message')
        response = send_sms(recipients, message)
        
        SMSLog.objects.create(
            recipients=", ".join(recipients),
            message=message, 
            status=response.get('status'), 
            response=response,
        )
        return redirect("sendMessage")
    context = {
        'all_sms': all_sms
    }
    return render(request, 'dashboard/sendMessage.html', context)

def bookings(request):
    rentals = Rental.objects.all()
    return render(request, 'dashboard/bookings.html', {'rentals': rentals})

def appointments(request):
    all_appointments = Appointment.objects.all()
    return render(request, 'dashboard/appointments.html', {'all_appointments': all_appointments})

def add_expenses(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_expenses')
    else:
        form = ExpenseForm()
    return render(request, 'dashboard/expenses/add_expense.html', {'form': form})

def view_expenses(request):
    car_id = request.GET.get('car', None)
    month = request.GET.get('month', None)
    expenses = Expense.objects.all()
    car_name = 'All Cars'
    month_name = 'All Months'
    if car_id:
        car = get_object_or_404(MyCar, id=car_id)
        expenses = expenses.filter(car_id=car_id)
        car_name = car.name
    if month:
        expenses = expenses.filter(month=month)
        month_name = month
        
    total_amount = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    totals = expenses.aggregate(
        total_amount_received=Sum('amount_received'),
        total_drivers_commission=Sum('drivers_commission'),
        total_other_expenses=Sum('other_expenses'),
        total_amount=Sum('amount')
    )
    
    all_totals = Expense.objects.aggregate(
        total_amount_received=Sum('amount_received'),
        total_drivers_commission=Sum('drivers_commission'),
        total_other_expenses=Sum('other_expenses'),
        total_amount=Sum('amount')
    )
    
    return render(request, 'dashboard/expenses/view_expenses.html', {
        'expenses': expenses,
        'cars': MyCar.objects.all(),
        'car': car_name,
        'month': month_name,
        'total_amount': total_amount,
        'totals': totals,
        'all_totals': all_totals,
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
        
        'cars': MyCar.objects.all(),
        
        
    })
    
    
def download_pdf(request):
    car_id = request.GET.get('car', None)
    month = request.GET.get('month', None)
    expenses = Expense.objects.all()
    car_name = 'All Cars'
    month_name = 'All Months'
    if car_id:
        car = get_object_or_404(MyCar, id=car_id)
        expenses = expenses.filter(car_id=car_id)
        car_name = car.name
    if month:
        expenses = expenses.filter(month=month)
        month_name = month
        
    totals = expenses.aggregate(
        total_amount_received=Sum('amount_received'),
        total_drivers_commission=Sum('drivers_commission'),
        total_other_expenses=Sum('other_expenses'),
        total_amount=Sum('amount')
    )
    
    all_totals = Expense.objects.aggregate(
        total_amount_received=Sum('amount_received'),
        total_drivers_commission=Sum('drivers_commission'),
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
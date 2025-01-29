from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    path('all_cars/', views.all_cars, name='all-cars'),
    path('all_cars_form/<slug:car_slug>/', views.all_cars_form, name='all-cars-form'),
    
    path('contact/', views.contact, name='contact'),
    path('sendMessage/', views.sendMessage, name='sendMessage'),
    path('send_driver_message/', views.sendDriverMessage, name='sendDriverMessage'),
    
    path('bookings/', views.bookings, name='bookings'),
    path('bookings/<int:rental_id>/update/', views.update_rentals, name='update-rental'),
    path('bookings/<int:rental_id>/complete/', views.complete_rental, name='complete-rental'),
    
    
    path('bookings_payments/', views.booking_payments, name='booking_payments'),
    path('booking_payment/<int:rental_id>/update/', views.update_rental_payment, name='update-rental-payment'),
    path('booking/<int:rental_id>/complete/', views.complete_rental_payment, name='complete-rental-payment'),
    path('print_book_receipt/<int:receipt_id>/', views.print_payment_receipt, name='print_payment_receipt'),
    
    
    path('appointments/', views.appointments, name='appointments'),
    path('appointments/<int:appointment_id>/assign_driver/', views.update_appointment, name='create-appointment'),
    path('appointments/<int:appointment_id>/complete/', views.complete_appointment, name='complete-appointment'),
    
    path('add_expense/', views.add_expenses, name='add_expense'),
    path('view_expenses/', views.view_expenses, name='view_expenses'),
    path('get_pdf/', views.get_pdf, name='get_pdf'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
    
    
    path('driver_list/', views.driver_list, name='driver-list'),
    path('driver/register/', views.register_driver, name='register-driver'),
    path('cars/<int:car_id>/assign_driver/', views.assign_driver, name='assign-driver'),
    path('driver_dashboard/<int:driver_id>/', views.driver_dashboard, name='driver-dashboard'),
    path('driver_detail/<int:driver_id>/', views.driver_detail, name='driver-detail'),
    
    
    path('create_receipt/', views.create_receipt, name='create-receipt'),
    path('print_receipt/<int:receipt_id>/', views.print_receipt, name='print-receipt'),

    path('newReceipt/', views.newReceipt, name='newReceipt'),
    
    path('customer_list/', views.customer_lists, name='customer-list'),
    
    # Agreements Urls
    path('agreementForm/', views.agreementForm, name='agreementForm'),
    
    path('pay_and_move_form/', views.pay_and_move_form, name='pay_and_move'),
    path('pay_and_move_lists/', views.pay_and_move_lists, name='pay_and_move_lists'),
    path('driveAndPay/<pdf>/', views.driveAndPay, name='driveAndPay'),
    
    path('driver_agreement_form/', views.driver_agreement_form, name='driver_agreement'),
    path('driver_agreement_lists/', views.driver_agreement_lists, name='driver_agreement_lists'),
    path('driverAgreement/<pdf>/', views.driverAgreement, name='driverAgreement'),
    
    path('new_contract_form/', views.new_contract_form, name='new_contract'),
    path('newContract/', views.newContract, name='newContract'),
    
    
    path('add_gallery/', views.add_gallery, name='add-gallery'),
    
]
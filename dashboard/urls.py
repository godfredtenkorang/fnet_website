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
    path('bookings/<int:rental_id>/delete/', views.delete_rentals, name='delete-rental'),
    path('bookings/<int:rental_id>/complete/', views.complete_rental, name='complete-rental'),
    path('print_book_receipt/<int:receipt_id>/', views.print_rental_receipt, name='print_rental_receipt'),
    
    
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
    
    # Driver
    path('driver_list/', views.driver_list, name='driver-list'),
    path('driver/register/', views.register_driver, name='register-driver'),
    path('cars/<int:car_id>/assign_driver/', views.assign_driver, name='assign-driver'),
    path('driver_dashboard/<int:driver_id>/', views.driver_dashboard, name='driver-dashboard'),
    path('driver_detail/<int:driver_id>/driver/', views.driver_detail, name='driver-detail'),
    path('driver_mileage_detail/<int:driver_id>/', views.driver_mileage_detail, name='driver-mileage-detail'),
    
    # Agent
    path('agent_list/', views.agent_list, name='agent-list'),
    path('agent/register/', views.register_agent, name='register-agent'),
    path('agent_detail/<int:agent_id>/', views.agent_detail, name='agent-detail'),
    path('agent-dashboard<int:agent_id>/', views.agent_dashboard, name='agent-dashboard'),
    
    
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
    
    
    path('boggas-drive-list/', views.new_contract_list, name='new_contract_list'),
    path('new-boggas-form/', views.new_contract_form, name='new_contract'),
    path('boggas-drive/<pdf>/', views.newContract, name='newContract'),
    
    
    path('add_gallery/', views.add_gallery, name='add-gallery'),
    
    
    path('cars_for_customer/', views.add_car_for_customer, name='add-car-for-customer'),
    path('customers_with_images_lists/', views.get_customers_with_images_upload, name='customers-with-images-lists'),
    path('get_images/<int:customer_id>/', views.get_customer_load_images, name='get-customer-load-images'),
    path('send_sms/', views.send_sms, name='send-sms-to-customer'),
    
    
    path('flight-booking/', views.flight_booking, name='flight-booking'),
    path('update-flight-booking/<int:airline_id>/', views.update_flight_booking, name='update_flight-booking'),
    
    path('all_profiles/', views.all_profiles, name='all_profiles'),
    
    path('all_reviews/', views.all_reviews, name='all_reviews'),
    
    path('users/', views.all_users, name='manage_users'),
    path('admin/block-user/<int:user_id>/', views.block_user, name='block_user'),
    path('admin/delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    
    path('all_services/', views.services, name='all_services'),
    
    path('all_payments/', views.all_payments, name='all_payments'),
    path('complete_payment/<int:payment_id>/', views.complete_rental_payment, name='complete_rental_payment'),
    
    path('properties_bookings/', views.property_bookings, name='properties_bookings'),
    path('properties_bookings/<int:property_id>/', views.approve_property, name='approve_property'),
    
    path('calculate_mileage/', views.calculate_mileage, name='calculate_mileage'),
]
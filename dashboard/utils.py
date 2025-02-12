import requests
from django.conf import settings

def send_sms(recipients, message):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TLGhana',
        "recipient[]": recipients,
        "message": message,
        "is_schedule": False,
        "schedule_date": ''
    }
    

    url = endpoint + '?key=' + apiKey
    
   
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error sending SMS: {e}")
        return None
    
def driver_send_sms(phone_numbers, message):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TLGhana',
        "recipient[]": phone_numbers,
        "message": message,
        "is_schedule": False,
        "schedule_date": ''
    }
    

    url = endpoint + '?key=' + apiKey
    
   
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error sending SMS: {e}")
        return None


def appointment_update_sms(phone_number, customer_name, status, schedule_date, pick_up_time, driver):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TLGhana',
        "recipient[]": phone_number,
        "message": f"Dear {customer_name}, your booking has been {status}. \n\n" "Schedule Details: \n" f"Date: {schedule_date} \n" f"Time: {pick_up_time} \n" f"Driver: {driver} \n\n" "We look forward to serving you!",
        "is_schedule": False,
        "schedule_date": ''
    }
    

    url = endpoint + '?key=' + apiKey
    
   
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error sending SMS: {e}")
        return None
    
def rental_update_sms(phone_number, customer_name, status, pick_up_time, drop_off_time, rental_date, return_date, location_category, town, driver, total_price):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TLGhana',
        "recipient[]": phone_number,
        "message": f"Dear {customer_name}, your booking has been {status}. \n\n" "Booking Details: \n" f"Pick up Time: {pick_up_time} \n" f"Drop off Time {drop_off_time} \n" f"Rental Date: {rental_date} \n" f"Return Date: {return_date} \n" f"Region: {location_category} \n" f"Town: {town} \n" f"Driver: {driver} \n" f"Amount: GH¢{total_price} \n\n" "Office Number 0550222888. \n\n or click on the link https://tlghana.com to view. \n\n" "Have a nice trip we are looking forword to serve you again! Thank you.",
        "is_schedule": False,
        "schedule_date": ''
    }
    

    url = endpoint + '?key=' + apiKey
    
   
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error sending SMS: {e}")
        return None
    

def rental_driver_update_sms(phone_number, first_name, rental_date, pick_up_time, drop_off_time, town, city, customer_name, customer_phone):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TLGhana',
        "recipient[]": phone_number,
        "message": "Trip Assignment \n\n" f"Dear {first_name},\n You have been assigned a trip. \n" "Details: \n" f"Date: {rental_date} \n" f"Time: {pick_up_time} - {drop_off_time} \n" f"Location: {town}, {city} \n" f"Client: {customer_name} ({customer_phone}) \n\n" "Please ensure the vehicle is ready and confirm receipt of this message. \n\n" "Thank you.",
        "is_schedule": False,
        "schedule_date": ''
    }
    

    url = endpoint + '?key=' + apiKey
    
   
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error sending SMS: {e}")
        return None
    
def rental_payment_update_sms(phone_number, customer_name, rental_date, return_date, driver):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TLGhana',
        "recipient[]": phone_number,
        "message": f"Dear {customer_name}, your booking has been confirmed. \n" "Booking Details: \n" f"Rental Date: {rental_date} \n" f"Return DateT: {return_date} \n" f"Driver: {driver} \n\n" "We look forward to serving you!",
        "is_schedule": False,
        "schedule_date": ''
    }
    

    url = endpoint + '?key=' + apiKey
    
   
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error sending SMS: {e}")
        return None
    
def driver_license_sms(phone_number, first_name, licence_number, licence_expiry_date):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TLGhana',
        "recipient[]": phone_number,
        "message": f"Dear {first_name}, your driver's license " f"(License Number: {licence_number}) is expiring on {licence_expiry_date}. " "Please renew it as soon as possible to avoid issues. \n" "Regards, \n" "TL Ghana." ,
        "is_schedule": False,
        "schedule_date": ''
    }
    

    url = endpoint + '?key=' + apiKey
    
   
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error sending SMS: {e}")
        return None
    
def driver_register_sms(phone_number, first_name):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TLGhana',
        "recipient[]": phone_number,
        "message": f"Dear {first_name}, thank you for being part of TL Ghana! Keep providing excellent service and enjoy exclusive benefits. Need support? Contact us anytime. Drive safe! - TL Ghana Team" ,
        "is_schedule": False,
        "schedule_date": ''
    }
    

    url = endpoint + '?key=' + apiKey
    
   
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error sending SMS: {e}")
        return None
    
    

def send_customer_sms_for_images(phone_number, name, customer_id):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TLGhana',
        "recipient[]": phone_number,
        "message": "Vehicle Condition Confirmation \n\n" f"Dear {name}, \n\n attached are pictures of the car before your rental. Please ensure it is returned in the same condition. Any damages may result in additional charges. \n\n" f"You can also view the car details here: https://tlghana.com/dashboard/get_images/{customer_id}/ \n\n" "For any questions, contact us at 0550222888. Thank you.",
        "is_schedule": False,
        "schedule_date": ''
    }
    

    url = endpoint + '?key=' + apiKey
    
   
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error sending SMS: {e}")
        return None
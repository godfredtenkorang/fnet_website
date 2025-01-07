import requests
from django.conf import settings

def send_sms(phone_number, customer_name, car_name, rental_date, return_date, total_price):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'GodeyTech',
        "recipient[]": phone_number,
        "message": f"Dear {customer_name}, your booking for {car_name} on \n" f"Rental Date: {rental_date} \n" f"Return Date: {return_date} \n" f"Total Price: GH¢{total_price} has been confirmed.",
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

def receive_sms(customer_name, customer_phone, car_name, rental_date, return_date, total_price):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'GodeyTech',
        "recipient[]": '0553912334',
        "message": f"New Car Booking from {customer_name} - {customer_phone}, booking for {car_name} on \n" f"Rental Date: {rental_date} \n" f"Return Date: {return_date} \n" f"Total Price: GH¢{total_price}",
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


def receive_contact(name, email, phone, message):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'GodeyTech',
        "recipient[]": '0553912334',
        "message": f"New Contact from {name} - {email} - {phone}, \n" f"Message: {message}" ,
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

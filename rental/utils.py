import requests
from django.conf import settings

def send_sms(phone_number, customer_name, appointment_date, appointment_time, purpose):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'GodeyTech',
        "recipient[]": phone_number,
        "message": f"Dear {customer_name}, your booking for  on \n" f"Appointment Date: {appointment_date} \n" f"Appointment Time: {appointment_time} \n" f"Purpose: {purpose}",
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

def receive_sms(customer_name, customer_phone, appointment_date, appointment_time, purpose):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'GodeyTech',
        "recipient[]": '0553912334',
        "message": f"New Appointment from {customer_name} - {customer_phone}, appointment on \n" f"Rental Date: {appointment_date} \n" f"Return Date: {appointment_time} \n" f"Purpose: {purpose}",
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

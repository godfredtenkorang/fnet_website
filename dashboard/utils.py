import requests
from django.conf import settings

def send_sms(recipients, message):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'GodeyTech',
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


def appointment_update_sms(phone_number, customer_name, appointment_date, appointment_time, driver):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'GodeyTech',
        "recipient[]": phone_number,
        "message": f"Dear {customer_name}, your booking has been confirmed. \n" "Appointment Details: \n" f"Date: {appointment_date} \n" f"Time: {appointment_time} \n" f"Driver: {driver} \n\n" "We look forward to serving you!",
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
        "sender": 'GodeyTech',
        "recipient[]": phone_number,
        "message": f"Dear {first_name}, your driver's license " f"(License Number: {licence_number}) is expiring on {licence_expiry_date}. " "Please renew it as soon as possible to avoid issues. \n" "Regards, \n" "Taxinet Ghana." ,
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
import requests
from django.conf import settings


def property_sms(phone_number, name, property_name):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TL GHANA',
        "recipient[]": phone_number,
        "message": f"Dear {name}, \n\nYour room booking for {property_name} is on pending. \n\n",
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
    
    
def receive_property_sms(name, phone, rent, check_in_date, check_in_time, check_out_date):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TL GHANA',
        "recipient[]": '0550222888',
        "message": f"New Propety Details: \n" f"Name: {name} \n" f"Phone Number: {phone}" f"Property: {rent} \n"  f"Check in Date: {check_in_date} \n" f"Check in Time: {check_in_time}" f"Check out Date: {check_out_date}",
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
    
    
def send_approve_sms(phone_number, name, property_name):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TL GHANA',
        "recipient[]": phone_number,
        "message": f"Dear {name}, \n\nYour room booking for {property_name} is approved. \n\n" "For more info, contact us on 0550222888 \n\nThank you!",
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
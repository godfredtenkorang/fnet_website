import random
import requests
from django.conf import settings
from .models import OTP

def generate_otp(length=6):
    """Generate a random numeric OTP of given length."""
    return ''.join(str(random.randint(0, 9)) for _ in range(length))


def send_otp_sms(phone_number, otp):
    """
    Send OTP to the given phone number.
    Replace the below code with your SMS provider's API integration.
    """
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TLGhana',
        "recipient[]": phone_number,
        "message": f"Your OTP is {otp}",
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
    
    
def send_otp(phone_number):
    otp = random.randint(100000, 999999)
    OTP.objects.update_or_create(phone=phone_number, defaults={"otp_code": otp})
    """
    Send OTP to the given phone number.
    Replace the below code with your SMS provider's API integration.
    """
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TLGhana',
        "recipient[]": phone_number,
        "message": f"Your OTP code is {otp}. Valid for 5 minutes.",
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
    
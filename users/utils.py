import random
import requests
from django.conf import settings
from .models import OTP

def generate_otp(length=6):
    """Generate a random numeric OTP of given length."""
    return ''.join(str(random.randint(0, 9)) for _ in range(length))


def send_otp_sms(phone_number, otp, username, password):
    """
    Send OTP to the given phone number.
    Replace the below code with your SMS provider's API integration.
    """
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TL GHANA',
        "recipient[]": phone_number,
        "message": f"Dear {username}, welcome to TLGHANA! \n" f"Use these details to login after entering this OTP: {otp} \n" f"Username: {username} \n" f"Password: {password} \n" "Thank you for choosing TLGHANA!",
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
        "sender": 'TL GHANA',
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
    
    
def send_payment_sms(phone_number, customer_name, total_price):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TL GHANA',
        "recipient[]": phone_number,
        "message": f"Dear {customer_name}, \n\n" f"Your payment of GH¢{total_price} has been received. Your booking is confirmed. \n\n" "Please note that cancellation of the trip will incur a 40 percent charge of the paid amount \n\n" "For any inquiries, contact 0550222888 \n\n" "Thank you for choosing us! Safe travels.",
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
    
    

def send_otp_whatsapp_mnotify(phone_number, otp, username, password):
    url = settings.MNOTIFY_WHATSAPP_URL
    headers = {
        "Authorization": f"Bearer {settings.MNOTIFY_WHATSAPP_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "recipient": phone_number,  # Must be in international format
        "message": f"Dear {username}, welcome to TLGHANA! \n" f"Use these details to login after entering this OTP: {otp} \n" f"Username: {username} \n" f"Password: {password} \n" "Thank you for choosing TLGHANA!",
        "type": "text"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.status_code == 200
    except Exception as e:
        print("MNotify WhatsApp error:", e)
        return False
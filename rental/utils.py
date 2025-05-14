import requests
from django.conf import settings

def send_sms(phone_number, customer_name, schedule_date, pick_up_time, drop_off_time, pick_up_location, drop_off_location, gps_address, purpose):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TL GHANA',
        "recipient[]": phone_number,
        "message": f"Dear {customer_name}, your booking is on pending. \n" "Schedule Details: \n" f"Schedule Date: {schedule_date} \n" f"Pick up Time: {pick_up_time} \n" f"Drop of Time: {drop_off_time} \n" f"Pick up Location: {pick_up_location} \n" f"Drop off Location: {drop_off_location} \n" f"GPS Address: {gps_address} \n" f"Note: {purpose} \n\n" "We look forward to serving you!",
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

def receive_sms(customer_name, customer_phone, schedule_date,  pick_up_time, drop_off_time, pick_up_location, drop_off_location, gps_address, purpose):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TL GHANA',
        "recipient[]": '0550222888',
        "message": f"New Schedule Details: \n" f"Customer Name: {customer_name} \n" f"Phone: {customer_phone} \n" f"Schedule Date: {schedule_date} \n" f"Pick up Time: {pick_up_time} \n" f"Drop of Time: {drop_off_time} \n" f"Pick up Location: {pick_up_location} \n" f"Drop off Location: {drop_off_location} \n" f"GPS Address: {gps_address} \n" f"Note: {purpose}",
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



import requests
from django.conf import settings

def payment_send_sms(phone_number, customer_name, car_name, rental_date, return_date, pick_up_location, drop_off_location, transaction_id, total_price):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TL GHANA',
        "recipient[]": phone_number,
        "message": f"Dear {customer_name}, your car booking for {car_name} is on pending. \n" "Rental Details: \n" f"Rental Date: {rental_date} \n" f"Return Date: {return_date} \n" f"Pick up Location: {pick_up_location} \n" f"Drop off Location: {drop_off_location} \n" f"Transaction ID: {transaction_id} \n" f"Total Price: GH¢{total_price}.",
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

def receive_payment_sms(customer_name, customer_phone, car_name, rental_date, return_date, pick_up_location, drop_off_location, transaction_id, total_price):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TL GHANA',
        "recipient[]": '0550222888',
        "message": f"New Car Booking Details: \n" f"Customer Name: {customer_name} \n"  f"Phone Number: {customer_phone} \n"  f"Car Booked: {car_name} \n" f"Rental Date: {rental_date} \n" f"Return Date: {return_date} \n" f"Pick up Location: {pick_up_location} \n" f"Drop off Location: {drop_off_location} \n" f"Transaction ID: {transaction_id} \n" f"Total Price: GH¢{total_price}",
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


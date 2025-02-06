import requests
from django.conf import settings

def send_sms(phone_number, full_name, airline):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TLGhana',
        "recipient[]": phone_number,
        "message": f"Dear {full_name}, your flight booking for {airline} is on pending. \n",
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

def receive_sms(full_name, phone_number, airline, category, trip_from, trip_to, trip_departure, trip_return, number_of_adults, number_of_children, number_of_infants):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TLGhana',
        "recipient[]": '0550222888',
        "message": f"New Flight Booking Details: \n\n" f"Customer Name: {full_name} \n" f"Phone Number: {phone_number} \n"  f"Flight Booked: {airline} \n" f"Category: {category}" f"From: {trip_from} \n" f"To: {trip_to} \n" f"Departure: {trip_departure} \n" f"Return: {trip_return} \n" f"Number of adults: {number_of_adults} \n" f"Number of childfred: {number_of_children} \n" f"Number of infants: {number_of_infants}",
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


def update_flight_sms(phone_number, full_name, status, airline, category, trip_from, trip_to, trip_departure, trip_return, number_of_adults, number_of_children, number_of_infants):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TLGhana',
        "recipient[]": phone_number,
        "message": f"Dear {full_name} \n\n" f"Your flight has been {status} \n\n" f"Flight Booked: {airline} \n" f"Category: {category} \n" f"From: {trip_from} \n" f"To: {trip_to} \n" f"Departure: {trip_departure} \n" f"Return: {trip_return} \n" f"Number of adults: {number_of_adults} \n" f"Number of childfred: {number_of_children} \n" f"Number of infants: {number_of_infants} \n\n" "Have a nice trip we are looking forword to serve you again! Thank you.",
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

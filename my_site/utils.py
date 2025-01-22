import requests
from django.conf import settings

def send_sms(phone_number, customer_name, car_name, rental_date, return_date, region, location_category, town, pick_up_time, drop_off_time, total_price):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TLGhana',
        "recipient[]": phone_number,
        "message": f"Dear {customer_name}, your car booking for {car_name} is on pending. \n" "Rental Details: \n" f"Rental Date: {rental_date} \n" f"Return Date: {return_date} \n" f"Region: {region} \n" f"Location: {location_category} \n" f"Town: {town} \n" f"Pick up Time: {pick_up_time} \n" f"Drop off Time: {drop_off_time} \n" f"Total Price: GH¢{total_price}.",
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

def receive_sms(customer_name, customer_phone, car_name, rental_date, return_date, region, location_category, town, pick_up_time, drop_off_time, total_price):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TLGhana',
        "recipient[]": '0244529353',
        "message": f"New Car Booking Details: \n" f"Customer Name: {customer_name} \n"  f"Phone Number: {customer_phone} \n"  f"Car Booked: {car_name} \n" f"Rental Date: {rental_date} \n" f"Return Date: {return_date} \n" f"Region: {region} \n" f"Location: {location_category} \n" f"Town: {town} \n" f"Pick up Time: {pick_up_time} \n" f"Drop off Time: {drop_off_time} \n" f"Total Price: GH¢{total_price}",
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
        "sender": 'TLGhana',
        "recipient[]": '0244529353',
        "message": f"New Contact Details: \n" f"Name: {name} \n"  f"Email: {email} \n"  f"Phone: {phone} \n" f"Message: {message}",
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


def get_location_based_price(car, location_category):
    """
    Calculate the price of the car based on the selected location category.
    :param car: Car instance
    :param location_category: Selected location category
    :return: Decimal price
    """
    if location_category == "within_kumasi":
        return car.price_within_kumasi
    elif location_category == "outside_kumasi_inside_ashanti":
        return car.price_outside_kumasi_inside_ashanti
    elif location_category == "outside_ashanti_to_next_region":
        return car.price_outside_ashanti_to_next_region
    elif location_category == "outside_ashanti_to_next_two_regions":
        return car.price_outside_ashanti_to_next_two_regions
    elif location_category == "outside_ashanti_to_next_three_regions":
        return car.price_outside_ashanti_to_next_three_regions
    else:
        raise ValueError("Invalid location category")
import requests
from django.conf import settings

def send_sms(phone_number, customer_name, car_name, rental_date, return_date, location_category, town, pick_up_time, drop_off_time, total_price):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TLGhana',
        "recipient[]": phone_number,
        "message": f"Dear {customer_name}, your car booking for {car_name} is on pending. \n" "Rental Details: \n" f"Rental Date: {rental_date} \n" f"Return Date: {return_date} \n" f"Region: {location_category} \n" f"Town: {town} \n" f"Pick up Time: {pick_up_time} \n" f"Drop off Time: {drop_off_time} \n" f"Total Price: GH¢{total_price}.",
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

def receive_sms(customer_name, customer_phone, car_name, rental_date, return_date, location_category, town, pick_up_time, drop_off_time, total_price):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'TLGhana',
        "recipient[]": '0550222888',
        "message": f"New Car Booking Details: \n" f"Customer Name: {customer_name} \n"  f"Phone Number: {customer_phone} \n"  f"Car Booked: {car_name} \n" f"Rental Date: {rental_date} \n" f"Return Date: {return_date} \n" f"Region: {location_category} \n" f"Town: {town} \n" f"Pick up Time: {pick_up_time} \n" f"Drop off Time: {drop_off_time} \n" f"Total Price: GH¢{total_price}",
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
        "recipient[]": '0550222888',
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
        return f"{car.price_within_kumasi} - {car.range_price_within_kumasi}"
    elif location_category == "ahafo_region":
        return f"{car.ahafo_region_price} - {car.range_price_ahafo_region}"
    elif location_category == "ashanti_region":
        return f"{car.ashanti_region_price} - {car.range_price_ashanti_region}"
    elif location_category == "bono_region":
        return f"{car.bono_region_price} - {car.range_price_bono_region}"
    elif location_category == "bono_east_region":
        return f"{car.bono_east_region_price} - {car.range_price_bono_east_region}"
    elif location_category == "central_region":
        return f"{car.central_region_price} - {car.range_price_central_region}"
    elif location_category == "eastern_region":
        return f"{car.eastern_region_price} - {car.range_price_eastern_region}"
    elif location_category == "greater_accra_region":
        return f"{car.greater_accra_region_price} - {car.range_price_greater_accra_region}"
    elif location_category == "northern_region":
        return f"{car.northern_region_price} - {car.range_price_northern_region}"
    elif location_category == "north_east_region":
        return f"{car.north_east_region_price} - {car.range_price_north_east_region}"
    elif location_category == "oti_region":
        return f"{car.oti_region_price} - {car.range_price_oti_region}"
    elif location_category == "savannah_region":
        return f"{car.savannah_region_price} - {car.range_price_savannah_region}"
    elif location_category == "upper_east_region":
        return f"{car.upper_east_region_price} - {car.range_price_upper_east_region}"
    elif location_category == "upper_west_region":
        return f"{car.upper_west_region_price} - {car.range_price_upper_west_region}"
    elif location_category == "volta_region":
        return f"{car.volta_region_price} - {car.range_price_volta_region}"
    elif location_category == "western_region":
        return f"{car.western_region_price} - {car.range_price_western_region}"
    elif location_category == "western_north_region":
        return f"{car.western_north_region_price} - {car.range_price_western_north_region}"
    else:
        raise ValueError("Invalid location category")
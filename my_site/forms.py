from django import forms
from .models import Driver, Car, Gallery

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['first_name', 'last_name', 'licence_number', 'phone_number', 'license_issue_date', 'licence_expiry_date', 'is_available']
        widgets = {
            'license_issue_date': forms.DateInput(attrs={'type': 'date'}),
            'licence_expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
        
class CarUpdateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['category', 'car_name', 'car_type', 'brand', 'seats', 'fuel_type', 'color', 'transmission', 'air_conditioning', 'year_manufactured', 'engine_capacity', 'airbag', 'price_per_hour', 'price_within_kumasi', 'range_price_within_kumasi', 'ahafo_region_price', 'range_price_ahafo_region', 'ashanti_region_price', 'range_price_ashanti_region', 'bono_region_price', 'range_price_bono_region', 'bono_east_region_price', 'range_price_bono_east_region', 'central_region_price', 'range_price_central_region', 'eastern_region_price', 'range_price_eastern_region', 'greater_accra_region_price', 'range_price_greater_accra_region', 'northern_region_price', 'range_price_northern_region', 'north_east_region_price', 'range_price_north_east_region', 'oti_region_price', 'range_price_oti_region', 'savannah_region_price', 'range_price_savannah_region', 'upper_east_region_price', 'range_price_upper_east_region', 'upper_west_region_price', 'range_price_upper_west_region', 'volta_region_price', 'range_price_volta_region', 'western_region_price', 'range_price_western_region', 'western_north_region_price', 'range_price_western_north_region', 'availability_status', 'year_registered', 'description', 'image1', 'image2', 'image3', 'image4']
        
        
class AddGalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['name', 'image']
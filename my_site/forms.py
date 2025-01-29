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
        fields = ['category', 'car_name', 'car_type', 'brand', 'seats', 'fuel_type', 'color', 'transmission', 'air_conditioning', 'year_manufactured', 'engine_capacity', 'airbag', 'price_per_hour', 'price_within_kumasi', 'ahafo_region_price', 'ashanti_region_price', 'bono_region_price', 'bono_east_region_price', 'central_region_price', 'eastern_region_price', 'greater_accra_region_price', 'northern_region_price', 'north_east_region_price', 'oti_region_price', 'savannah_region_price', 'upper_east_region_price', 'upper_west_region_price', 'volta_region_price', 'western_region_price', 'western_north_region_price', 'availability_status', 'year_registered', 'description', 'image1', 'image2', 'image3', 'image4']
        
        
    def __init__(self, *args, **kwargs):
        super(CarUpdateForm, self).__init__(*args, **kwargs)
        self.fields['image1'].required = False  # Allow updating without changing the image
        self.fields['image2'].required = False  # Allow updating without changing the image
        self.fields['image3'].required = False  # Allow updating without changing the image
        self.fields['image4'].required = False  # Allow updating without changing the image
        
        
class AddGalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['name', 'image']
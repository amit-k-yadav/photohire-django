from django import forms 
from .models import *
  
class HotelForm(forms.ModelForm): 
  
    class Meta: 
        model = Hotel 
        fields = ['name', 'hotel_Main_Img'] 

class ImageForm(forms.ModelForm): 
  
    class Meta: 
        model = Images
        fields = ['user_id','tags']
from django import forms 
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

class Tes(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=('profile_views','user')

class editprofileform(UserChangeForm):
    class Meta:
        model=Profile
        fields=(
        "first_name",
        "last_name",
	'bio',
)
    def clean_password(self):
        return self.clean_password

class LoginForm(forms.Form):
	email=forms.CharField(max_length=30)
	password=forms.CharField(widget=forms.PasswordInput, max_length=40)


class ProfileCreationForm(forms.Form):
    birth_date=forms.DateField(help_text='Format: YYYY-MM-DD')

class UserSignUpForm(UserCreationForm):
        is_photographer=forms.BooleanField()
        class Meta:
            model = User
            fields = ( 'first_name', 'last_name', 'username','password1', 'password2' )


        def clean_password2(self):
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
            return password2

class ImagesForm(forms.ModelForm): 

	class Meta: 
		model = Images
		fields = ['image', 'user_id', 'tags'] 

class RatingsForm(forms.ModelForm):
    class Meta:
        model = Ratings
        fields = ['user_id', 'rating', 'review']

class BookingsForm(forms.ModelForm):
    booking_from = forms.DateField(input_formats=['%d-%m-%Y'])
    booking_to = forms.DateField(input_formats=['%d-%m-%Y'])
    class Meta:
        model = Bookings
        fields = ['user_id', 'photographer_id', 'event', 'booking_from', 'booking_to']
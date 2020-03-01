from django import forms 
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm



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

class UserCreationForm(UserCreationForm):
#        first_name = forms.CharField(max_length=30, required=True, help_text='Optional.')
#        last_name = forms.CharField(max_length=30, required=True, help_text='Optional.')
#        email = forms.EmailField(max_length=254, required=True,help_text='Required. Inform a valid email address.')

        #birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
        class Meta:
            model = User
            fields = ( 'first_name', 'last_name', 'username','password1', 'password2' )









#
#	email=forms.CharField(max_length=30)
#	password=forms.CharField(widget=forms.PasswordInput, max_length=40)
#	first_name = forms.CharField(max_length=20)
#	last_name = form.CharField(max_length=20)

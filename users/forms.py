from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1',
                    'password2']

					
class CustomLoginForm(forms.ModelForm):

    class Meta:
	    model = User
        fields = ('username', 'password')
        widgets = {
                    'username': forms.TextInput(attrs={
                    'class':'textinputclass', 'placeholder': 'Username'}),
                    'password':forms.TextInput(attrs={
                    'class':'textinputclass', 'type':'password', placeholder': 'Password'})}
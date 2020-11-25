from django.forms import widgets
from user.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import TextInput, EmailInput, Select, FileInput

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=512, label='User Name')
    email = forms.EmailField(max_length=512, label='Email')
    first_name = forms.CharField(max_length=512, label='First Name')
    last_name = forms.CharField(max_length=512, label='Last Name')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', )

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': TextInput(attrs={'class': 'input', 'placeholder': 'username'}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': 'email'}),
            'first_name': TextInput(attrs={'class': 'input', 'placeholder': 'first_name'}), 
            'last_name': TextInput(attrs={'class': 'input', 'placeholder': 'last_name'}),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city', 'country', 'image')
        widgets = {
            'phone': TextInput(attrs={'class': 'input','placeholder':'phone'}),
            'address': TextInput(attrs={'class': 'input','placeholder':'address'}),
            'city': TextInput(attrs={'class': 'input','placeholder':'city'}),
            'country': TextInput(attrs={'class': 'input','placeholder':'country' }),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image', }),
        }
from dataclasses import field
from django.db import models
from .models import Profile, Messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import  User
from django.forms import ModelForm      #, FloatField, FloatField, HiddenInput



class RegisterForm(UserCreationForm):
    email = models.EmailField(unique=True)
    class Meta:
        model = User
        fields = ['first_name','last_name','username','password1','password2']


class LoginForm(ModelForm):
    email = models.EmailField(unique=True)
    class Meta:
        model = User
        fields = ['username', 'password']

class updateUserForm(ModelForm):
    email = models.EmailField(unique=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name','email',
                  'username',]

class updateProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','avater','nickname']


class WriteUpdateMessageForm(ModelForm):
    # x = FloatField(widget=HiddenInput())
    # y = FloatField(widget=HiddenInput())
    class Meta:
        model = Messages
        fields = ['text', 'file', 'image']
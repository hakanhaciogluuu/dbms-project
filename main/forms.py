from django import forms
from django.contrib.auth.forms import  UserChangeForm
from django.contrib.auth.models import User
from django.forms import EmailInput



class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)
        widgets = {
            'email'     : EmailInput(attrs={'class': 'input','placeholder':'email'}),
        }
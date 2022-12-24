from django.contrib.auth.forms import  UserChangeForm
from django.contrib.auth.models import User
from django.forms import EmailInput,ModelForm, ModelChoiceField
from main.models import Sepet, Adres, Sehirler


class SepetForm(ModelForm):
    class Meta:
        model = Sepet
        fields = ['miktar']


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)
        widgets = {
            'email'     : EmailInput(attrs={'class': 'input','placeholder':'email'}),
        }

class AddressForm(ModelForm):
    class Meta:
        model = Adres
        fields = ['adres_adi', 'adres', 'sehir']
from django.contrib.auth.forms import  UserChangeForm
from django.contrib.auth.models import User
from django.forms import EmailInput,ModelForm
from main.models import Sepet, Adres, CreditCard, Siparis, Yorum


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

class CreditCardForm(ModelForm):
    class Meta:
        model = CreditCard
        fields = ['card_number', 'expiration_date_month','expiration_date_year', 'cvv']


class SiparisForm(ModelForm):
    class Meta:
        model = Siparis
        fields = ['first_name','last_name','telefon','adres','kredi_karti']


class YorumForm(ModelForm):
    class Meta:
        model = Yorum
        fields = ['text', 'image']
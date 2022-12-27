from django.db import models
from django.forms import ModelForm
from django.utils.text import slugify
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from django.apps import apps

# Create your models here.

#TEMA -> temaId, temaAdı, ...

class Renk(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"

class Beden(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.name}"

class Tema(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(null=False, blank=True, unique=True, db_index=True,editable=False)
    def __str__(self):
        return f"{self.name}"
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

#CATEGORY -> categoryId, temaId, categoryAdı,..
class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(null=False, blank=True, unique=True, db_index=True,editable=False)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name}"
    def save(self, *args, **kwargs):
         self.slug = slugify(self.name)
         super().save(*args, **kwargs)




class Urun(models.Model):
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    renk = models.ForeignKey(Renk, on_delete=models.CASCADE)
    beden = models.ForeignKey(Beden, on_delete=models.CASCADE)
    aciklama = models.TextField(blank=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=False, blank=True, unique=True, db_index=True,editable=False)
    available = models.BooleanField(default=True)
    stok = models.PositiveIntegerField()
    fiyat = MoneyField(max_digits=10, default_currency='TL')
    barkod = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.name}"
    def save(self, *args, **kwargs):
         self.slug = slugify(self.name)
         super().save(*args, **kwargs)

    @property
    def get_images(self):
        return self.images.all()

        

class UrunFotograf(models.Model):
    urun = models.ForeignKey(Urun, on_delete=models.CASCADE, default= 1, related_name='images')
    image = models.ImageField(upload_to="urunler")


class Sepet(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    urun = models.ForeignKey(Urun, on_delete= models.SET_NULL, null=True)
    miktar = models.IntegerField()

    @property
    def amount(self):
        return(self.miktar * self.urun.fiyat)

    @property
    def fiyat(self):
        return (self.urun.fiyat)




class Sehirler(models.Model):
    sehir_adi = models.CharField(max_length=50)
    def __str__(self):
        return self.sehir_adi


class Adres(models.Model):
    adres_adi = models.CharField(max_length=50)
    adres = models.TextField(max_length=400)
    sehir = models.ForeignKey(Sehirler, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.adres_adi

    @property
    def username(self):
        return(self.user.username)
    
    @property
    def sehir_adi(self):
        return(self.sehir.sehir_adi)

class Yorum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    yorum_urun = models.ForeignKey(Urun, on_delete=models.CASCADE, default= 1)
    text = models.TextField(max_length=300)

    @property
    def urun_adi(self):
        return(self.yorum_urun.name)
    
    @property
    def username(self):
        return(self.user.username)


class YorumFotograf(models.Model):
    yorum = models.ForeignKey(Yorum, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="yorumlar")

    @property
    def get_images(self):
        return self.images.all()


class Favoriler(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    urun = models.ForeignKey(Urun, on_delete=models.CASCADE, default= 1)


class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    expiration_date_month = models.CharField(max_length=2 ,default=1)
    expiration_date_year = models.CharField(max_length=2, default=24)
    cvv = models.CharField(max_length=3)

DURUM_CHOICES = (
    ('onay_bekliyor', 'Onay Bekliyor'),
    ('kargolandi', 'Kargolandı'),
    ('teslim_edildi', 'Teslim Edildi'),
    ('iade_edildi', 'İade Edildi'),
)

class Siparis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=10, default='no-name')
    last_name = models.CharField(max_length=10, default='no-name')
    telefon = models.CharField(blank=True, max_length=20)
    urunler = models.ManyToManyField(Urun, through='SiparisUrun')
    adres = models.ForeignKey(Adres, on_delete=models.CASCADE)
    kredi_karti = models.ForeignKey(CreditCard, on_delete=models.CASCADE)
    tarih = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(blank=True, max_length=20)
    durum = models.CharField(max_length=50, choices=DURUM_CHOICES, default='onay_bekliyor')
    toplam_tutar = MoneyField(max_digits=10, default_currency='TL')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SiparisUrun(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    siparis = models.ForeignKey(Siparis, on_delete=models.CASCADE)
    urun = models.ForeignKey(Urun, on_delete=models.CASCADE)
    miktar = models.PositiveIntegerField()
    fiyat = MoneyField(max_digits=10, default_currency='TL')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
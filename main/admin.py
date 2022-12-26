from django.contrib import admin
from django.shortcuts import get_object_or_404
from .models import Renk,Beden,Tema,Category,Urun,UrunFotograf,Sepet,Sehirler,Adres,YorumFotograf,Yorum,Favoriler
from django.db.models import Count

class UrunFotografAdmin(admin.StackedInline):
    model = UrunFotograf

class YorumFotografAdmin(admin.StackedInline):
    model = YorumFotograf

class YorumAdmin(admin.ModelAdmin):
    list_display = ['yorum_urun', 'user', 'text']
    inlines = [YorumFotografAdmin]
    class Meta:
        model = Yorum

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name","slug","tema")
    list_filter =("tema",)

class TemaAdmin(admin.ModelAdmin):
    list_display = ("name","slug")


class UrunAdmin(admin.ModelAdmin):
    list_display = ['name', 'tema', 'slug', 'category', 'fiyat', 'stok', 'available', 'created_at','updated_at']
    list_filter = ['available', 'created_at', 'updated_at', 'category']
    list_editable = ['fiyat', 'stok', 'available']
    inlines = [UrunFotografAdmin]
    class Meta:
        model = Urun

class SepetAdmin(admin.ModelAdmin):
    list_display = ['user', 'urun', 'miktar', 'amount']
    list_filter = ['user']

class AdresAdmin(admin.ModelAdmin):
    list_display = ['username', 'sehir', 'adres_adi', 'sehir_adi']

class FavorilerAdmin(admin.ModelAdmin):
    list_display = ['user', 'urun']


class SehirlerAdmin(admin.ModelAdmin):
    list_display = ['sehir_adi'] 


class FavorilereEklenenUrunlerAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        # Alt kategoriye göre filtreleme yapmak için, Category modelinden bir category instance'ı alın.
        categories = Category.objects.all()

        favorilere_eklenen_urunler = []
        for category in categories:
             urunler = Favoriler.objects.filter(urun__category=category.id)

            # Bu queryset'ten, en çok favorilere eklenen ilk üç ürünü bulun.
        favorilere_eklenen_urunler += urunler.values('urun').annotate(count=Count('urun')).order_by('-count')[:3]

        # İşlenmiş favorilere eklenen ürünleri döndürün.
        return favorilere_eklenen_urunler

# View'ı bir Django admin view olarak kaydedin.
admin.site.register(Renk)
admin.site.register(Beden)
admin.site.register(Tema, TemaAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Urun,UrunAdmin)
admin.site.register(Yorum,YorumAdmin)
admin.site.register(Sepet,SepetAdmin)
admin.site.register(Adres, AdresAdmin)
admin.site.register(Sehirler, SehirlerAdmin)
admin.site.register(Favoriler, FavorilereEklenenUrunlerAdmin)

# Register your models here.

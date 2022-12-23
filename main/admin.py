from django.contrib import admin

from .models import Renk,Beden,Tema,Category,Urun,UrunFotograf,Sepet,Sehirler,Adres,YorumFotograf,Yorum,Favoriler

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

admin.site.register(Renk)
admin.site.register(Beden)
admin.site.register(Tema, TemaAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Urun,UrunAdmin)
admin.site.register(Yorum,YorumAdmin)
admin.site.register(Sepet,SepetAdmin)
admin.site.register(Adres, AdresAdmin)
admin.site.register(Sehirler, SehirlerAdmin)
admin.site.register(Favoriler, FavorilerAdmin)

# Register your models here.

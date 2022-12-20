from django.contrib import admin

from .models import Renk,Beden,Tema,Category,Urun,UrunFotograf



class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name","slug","tema")
    list_filter =("tema",)

class TemaAdmin(admin.ModelAdmin):
    list_display = ("name","slug")


class ProductImagesInline(admin.StackedInline):
    model = UrunFotograf

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'tema', 'slug', 'category', 'fiyat', 'stok', 'available', 'created_at','updated_at']
    list_filter = ['available', 'created_at', 'updated_at', 'category']
    list_editable = ['fiyat', 'stok', 'available']
    inlines = [ProductImagesInline]





admin.site.register(Renk)
admin.site.register(Beden)
admin.site.register(Tema, TemaAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Urun)

# Register your models here.
from django.urls import path
from . import views



urlpatterns = [
    path("", views.index, name= "home"),
    path("category/<slug:slug>", views.urunler, name= "urunler"),
    path("urun/<slug:slug>", views.urun_detay, name="urun_detay"),
    #####account
    path("login", views.login_request, name= "login"),
    path("register", views.register_request, name= "register"),
    path("logout", views.logout_request, name= "logout"),
    path("search_product", views.search_product, name= "search_product"),
    path("sepet", views.sepet, name= "sepet"),
    path('sepete_ekle/<int:id>', views.sepete_ekle, name='sepete_ekle'),
    path('sepetten_sil/<int:id>', views.sepetten_sil, name='sepetten_sil')
]
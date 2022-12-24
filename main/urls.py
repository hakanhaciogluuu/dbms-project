from django.urls import path
from . import views



urlpatterns = [
    path("", views.index, name= "home"),
    path("category/<slug:slug>", views.urunler, name= "urunler"),
    path("urun/<slug:slug>", views.urun_detay, name="urun_detay"),
    path("search_product", views.search_product, name= "search_product"),
    #####account
    path("login", views.login_request, name= "login"),
    path("register", views.register_request, name= "register"),
    path("logout", views.logout_request, name= "logout"),
    #####favoriler
    path("favoriler", views.favoriler, name= "favoriler"),
    path('favorilere_ekle/<int:id>', views.favorilere_ekle, name='favorilere_ekle'),
    path('favorilerden_sil/<int:id>', views.favorilerden_sil, name='favorilerden_sil'),
    #####Sepet
    path("sepet", views.sepet, name= "sepet"),
    path('sepete_ekle/<int:id>', views.sepete_ekle, name='sepete_ekle'),
    path('sepetten_sil/<int:id>', views.sepetten_sil, name='sepetten_sil'),
    #####Profil
    path("profile", views.profile, name= "profile"),
    path('profile_sil/<int:id>', views.profile_sil, name='profile_sil'),
    path('profile_email_guncelle', views.profile_email_guncelle, name='profile_email_guncelle'),
    path('password/', views.user_password, name='user_password'),
    path('adres_ekle/', views.adres_ekle, name='adres_ekle'),
]
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
    path('favorilere_eklenen_urunler_kategori/', views.favorilere_eklenen_urunler_kategori, name='favorilere_eklenen_urunler_kategori'),
    #####Sepet
    path("sepet", views.sepet, name= "sepet"),
    path('sepete_ekle/<int:id>', views.sepete_ekle, name='sepete_ekle'),
    path('sepetten_sil/<int:id>', views.sepetten_sil, name='sepetten_sil'),
    #####Profil
    path("profile", views.profile, name= "profile"),
    path('profile_sil/<int:id>', views.profile_sil, name='profile_sil'),
    path('profile_email_guncelle', views.profile_email_guncelle, name='profile_email_guncelle'),
    path('password/', views.user_password, name='user_password'),
    #######Adres
    path('add_address', views.add_address, name='add_address'),
    path('address_list', views.address_list, name='address_list'),
    path('delete_address/<int:address_id>', views.delete_address, name='delete_address'),
    #######Credit-Card
    path('add_credit_card/', views.add_credit_card, name='add_credit_card'),
    path('credit_card_list/', views.credit_card_list, name='credit_card_list'),
    path('delete_credit_card/<int:credit_card_id>/', views.delete_credit_card, name='delete_credit_card'),
    #######Siparis
    path('siparis/', views.siparis, name='siparis'),
    path('siparislerim/', views.siparislerim, name='siparislerim'),
    path('siparis_detay/<int:id>', views.siparis_detay, name='siparis_detay'),
    #######Yorum
    path('yorum_ekle/<int:urun_id>/', views.yorum_ekle, name='yorum_ekle'),
    path('yorumlar', views.yorumlar, name='yorumlar'),
    path('yorum_sil/<int:id>', views.yorum_sil, name='yorum_sil'),
]
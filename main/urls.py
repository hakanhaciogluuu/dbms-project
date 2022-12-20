from django.urls import path
from . import views

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/index
# http://127.0.0.1:8000/blogs
# http://127.0.0.1:8000/blogs/2



urlpatterns = [
    path("", views.index, name= "home"),
    path("category/<slug:slug>", views.urunler, name= "urunler"),
]
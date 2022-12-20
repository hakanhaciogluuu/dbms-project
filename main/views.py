from django.http.response import HttpResponse
from django.shortcuts import render
from main.models import Category, Urun

# Create your views here.


def index(request):
    context = {
        "categories" : Category.objects.all()
    }
    return render(request, "index.html", context)

def urunler(request, slug):
    context = {
        "urunler": Urun.objects.filter(category__slug = slug),
        "categories" : Category.objects.all()
    }
    return render(request,"urunler.html", context)
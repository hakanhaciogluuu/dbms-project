from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from main.models import Category, Urun, UrunFotograf
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.


#hesap işlemleri

def login_request(request):
    if request.user.is_authenticated:
        return redirect("home")
    context = {
        "categories" : Category.objects.all()
    }
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "login.html", {
                "error": "username ya da password yanlis" 
            })
    return render(request, "login.html", context)

def register_request(request):
    if request.user.is_authenticated:
        return redirect("home")
    context = {
        "categories" : Category.objects.all()
    }
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]

        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(request, "register.html", {"error": "username kullanılıyor."})
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, "register.html", {"error": "email kullanılıyor."})
                else:
                    user = User.objects.create_user(username=username, email=email,first_name=firstname, last_name=lastname,password=password)
                    user.save()
                    return redirect("login")
        else:
            return render(request, "register.html", {"error":"parolar eşleşmiyor."})
    return render(request, "register.html",context)

def logout_request(request):
    logout(request)
    return redirect("home")










def index(request):
    context = {
        "categories" : Category.objects.all()
    }
    return render(request, "index.html", context)

def urunler(request, slug):
    context = {
        "urunler": Urun.objects.filter(category__slug = slug),
        "fotograflar": UrunFotograf.objects.all(),
        "categories" : Category.objects.all()
    }
    return render(request,"urunler.html", context)
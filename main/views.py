from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from main.models import Category, Urun, UrunFotograf, SepetForm, Sepet, Favoriler
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.forms import UserUpdateForm

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


#Search


def search_product(request):

    if request.method == "POST":
        search = request.POST['search']
        categories = Category.objects.all()
        urunler = Urun.objects.filter(Q(name__contains=search) | Q(barkod__contains = search))
        context = {
            "categories" : categories,
            'search' : search,
            'urunler' : urunler
        }
        return render(request, "search.html" ,context)
    else:
        return render(request, "search.html" ,context)








def index(request):
    current_user = request.user
    request.session['sepet_urunler'] = Sepet.objects.filter(user_id=current_user.id).count()
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


def urun_detay(request , slug):
    urun = Urun.objects.get(slug=slug)
    return render(request,"urun_detay.html",{
        "urun" : urun,
        "categories" : Category.objects.all()
    })



@login_required(login_url='/login')
def favoriler(request):
    categories = Category.objects.all()
    user = request.user
    favoriler = Favoriler.objects.filter(user_id = user.id)


    context = {
        'favoriler':favoriler,
        'categories': categories,
    }
    
    return render(request, 'favoriler.html',context)

@login_required(login_url='/login')
def favorilere_ekle(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    urunkontrol = Favoriler.objects.filter(urun_id = id, user_id = current_user.id)
    if urunkontrol:
        messages.success(request, "Ürün zaten favorilerinde.")
        return HttpResponseRedirect(url)
    else:
        if request.method == 'POST':
            data = Favoriler()
            data.user_id = current_user.id
            data.urun_id = id
            data.save()
        messages.success(request, "Ürün favorilere eklendi.")
        return HttpResponseRedirect(url)

@login_required(login_url='/login')
def favorilerden_sil(request, id):
    Favoriler.objects.filter(id=id).delete()
    messages.success(request, 'Ürün Favorilerden Silinmiştir.')
    return HttpResponseRedirect("/favoriler")






@login_required(login_url='/login')
def sepet(request):
    categories = Category.objects.all()
    user = request.user
    sepet = Sepet.objects.filter(user_id = user.id)
    total = 0

    for rs in sepet:
        total += rs.urun.fiyat * rs.miktar

    context = {
        'sepet':sepet,
        'categories': categories,
        'total': total
    }
    
    return render(request, 'sepet.html',context)


@login_required(login_url='/login')
def sepete_ekle(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user

    urunkontrol = Sepet.objects.filter(urun_id = id, user_id=current_user.id)
    if request.method == 'POST':
        form = SepetForm(request.POST)
        if form.is_valid():
            if urunkontrol:
                data = Sepet.objects.get(urun_id =id)
                data.miktar += form.cleaned_data['miktar']
                data.save()
            else:
                data = Sepet()
                data.user_id = current_user.id
                data.urun_id = id
                data.miktar = form.cleaned_data['miktar']
                data.save()
            request.session['sepet_urunler'] = Sepet.objects.filter(user_id=current_user.id).count()
            messages.success(request, "Ürün sepete eklendi.")
            return HttpResponseRedirect(url)


@login_required(login_url='/login')
def sepetten_sil(request, id):
    current_user = request.user
    Sepet.objects.filter(id=id).delete()
    request.session['sepet_urunler'] = Sepet.objects.filter(user_id=current_user.id).count()
    messages.success(request, 'Ürün Sepetten Silinmiştir.')
    return HttpResponseRedirect("/sepet")

@login_required(login_url='/login')
def profile(request):
    context = {
        'user' : request.user,
        'categories': Category.objects.all()
    }
    return render(request, 'profile.html', context)


@login_required(login_url='/login')
def profile_sil(request, id):
    User.objects.filter(id=id).delete()
    messages.warning(request, 'Hesabınız silinmiştir.')
    return HttpResponseRedirect("/login")

@login_required(login_url='/login') # Check login
def profile_email_guncelle(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user) # request.user is user  data
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/profile')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        context = {
            'category': category,
            'user_form': user_form,
        }
        return render(request, 'profile_email_guncelle.html', context)

@login_required(login_url='/login') # Check login
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/profile')
        else:
            messages.error(request, 'Please correct the error below.<br>'+ str(form.errors))
            return HttpResponseRedirect('/password')
    else:
        #category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'profile_parola_guncelle.html', {'form': form, #'category': category
                       })